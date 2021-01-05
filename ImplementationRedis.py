import re
from gevent.pool import Pool
from gevent.server import StreamServer
from expiring_dict import ExpiringDict
from collections import namedtuple
from io import BytesIO
import os
import logging

logger = logging.getLogger(__name__)


class CommandError(Exception):
    pass


class Disconnect(Exception):
    pass


Error = namedtuple('Error', ('message',))


class DataHandler(object):
    def __init__(self):
        self.handlers = {
            '+': self.handle_simple_string,
            '-': self.handle_error,
            ':': self.handle_integer,
            '$': self.handle_string,
            '*': self.handle_array,
            '%': self.handle_dict}

    def handle_request(self, socket_file):
        first_byte = socket_file.read(1).decode("utf-8")
        if not first_byte:
            raise Disconnect()

        try:
            return self.handlers[first_byte](socket_file)
        except KeyError:
            raise CommandError('bad request')

    def handle_simple_string(self, socket_file):
        data = socket_file.readline().decode('utf-8').rstrip('\r\n')
        return data

    def handle_error(self, socket_file):
        return Error(socket_file.readline().decode('utf-8').rstrip('\r\n'))

    def handle_integer(self, socket_file):
        data = int(socket_file.readline().decode('utf-8').rstrip('\r\n'))
        return data

    def handle_string(self, socket_file):
        length = int(socket_file.readline().decode('utf-8').rstrip('\r\n'))
        if length == -1:
            return None
        length += 2
        return socket_file.read(length)[:-2].decode('utf-8')

    def handle_array(self, socket_file):
        num_elements = int(socket_file.readline().decode('utf-8').rstrip('\r\n'))
        r = []
        for _ in range(num_elements):
            r.append(self.handle_request(socket_file))
        return r

    def handle_dict(self, socket_file):
        num_items = int(socket_file.readline().decode('utf-8').rstrip('\r\n'))
        elements = [self.handle_request(socket_file)
                    for _ in range(num_items * 2)]
        return dict(zip(elements[::2], elements[1::2]))

    def write_response(self, socket_file, data):
        buf = BytesIO()
        self._write(buf, data)
        buf.seek(0)
        socket_file.write(buf.getvalue())
        socket_file.flush()

    def _write(self, buf, data):
        if isinstance(data, str):
            buf.write(f'${len(data)}\r\n{data}\r\n'.encode('utf-8'))
        elif isinstance(data, bytes):
            buf.write(f'${len(data)}\r\n{data.decode("utf-8")}\r\n'.encode('utf-8'))
        elif isinstance(data, int):
            buf.write(f':{data}\r\n'.encode('utf-8'))
        elif isinstance(data, Error):
            buf.write(f'-{data.message}\r\n'.encode("utf-8"))
        elif isinstance(data, (list, tuple)):
            buf.write(f'*{len(data)}\r\n'.encode("utf-8"))
            for item in data:
                self._write(buf, item)
        elif isinstance(data, dict):
            buf.write(f'%{len(data)}\r\n')
            for key in data:
                self._write(buf, key)
                self._write(buf, data[key])
        elif data is None:
            buf.write('$-1\r\n'.encode('utf-8'))
        else:
            raise CommandError('unrecognized type: %s' % type(data))


class Server(object):
    def __init__(self, host=None, port=None, max_clients=None):
        if not host:
            host = os.getenv('HOST', '0.0.0.0')
        if not port:
            port = os.getenv('PORT', 31337)
        if not max_clients:
            max_clients = os.getenv('MAX_CLIENTS', 15)
        self._pool = Pool(int(max_clients))
        self._server = StreamServer(
            (host, int(port)),
            self.connection_handler,
            spawn=self._pool)

        self._protocol = DataHandler()
        self._kv = ExpiringDict()

        self._commands = self.get_commands()

    def get_commands(self):
        return {
            'GET': self.get,
            'SET': self.set,
            'DEL': self.delete,
            'KEYS': self.keys,
            'FLUSHDB': self.flush,
            'EXPIRE': self.expire,
            'HGET': self.hget,
            'HSET': self.hset,
            'LSET': self.lset,
            'RPUSH': self.rpush,
            'LPUSH': self.lpush,
            'LRANGE': self.lrange,
            'LINDEX': self.lindex
        }

    def connection_handler(self, conn, address):
        logger.info('Connection received: %s:%s' % address)
        socket_file = conn.makefile('rwb')

        while True:
            try:
                data = self._protocol.handle_request(socket_file)
            except Disconnect:
                logger.info('Client went away: %s:%s' % address)
                break
            try:
                resp = self.get_response(data)
            except CommandError as exc:
                logger.exception('Command error')
                resp = Error(exc.args[0])

            self._protocol.write_response(socket_file, resp)

    def run(self):
        self._server.serve_forever()

    def get_response(self, data):
        if not isinstance(data, list):
            try:
                data = data.split()
            except:
                raise CommandError('Request must be list or simple string.')

        if not data:
            raise CommandError('Missing command')

        command = data[0].upper()
        if command not in self._commands:
            raise CommandError('Unrecognized command: %s' % command)
        else:
            logger.debug('Received %s', command)
        try:
            response = self._commands[command](*data[1:])
        except TypeError:
            raise CommandError(f'ERR wrong number of arguments for {command.lower()} command')
        return response

    def get(self, key):
        return self._kv.get(key)

    def set(self, key, value):
        self._kv[key] = value
        return '1'

    def delete(self, key):
        if key in self._kv:
            del self._kv[key]
            return 1
        return 0

    def keys(self, pattern):
        r = []
        if pattern == '*':
            pattern = '\w*'
        for k in self._kv.keys():
            if re.match(pattern, k):
                r.append(k)
        return r

    def flush(self):
        kvlen = len(self._kv)
        self._kv.clear()
        return str(kvlen)

    def expire(self, key, ttl):
        value = self._kv.get(key, None)
        if value:
            del self._kv[key]
            self._kv.ttl(key, value, float(ttl))
            return 1
        return 0

    def hset(self, key, field, value):
        self._kv.setdefault(key, {})
        self._kv[key][field] = value
        return 1

    def hget(self, k, field):
        if self._kv.get(k):
            return self._kv[k].get(field)

    def lset(self, key, index, value):
        self._kv.setdefault(key, [])
        self._kv[key][int(index)] = value
        return 'OK'

    def rpush(self, key, *value):
        self._kv.setdefault(key, [])
        for v in value:
            self._kv[key].append(v)
        return len(self._kv[key])

    def lpush(self, key, *value):
        self._kv.setdefault(key, [])
        for v in value:
            self._kv[key].insert(0, v)
        return len(self._kv[key])

    def lrange(self, key, start, end):
        if isinstance(self._kv.get(key), list):
            if end == '-1':
                return self._kv[key][int(start):]
            return self._kv[key][int(start):int(end) + 1]
        return None

    def lindex(self, key, index):
        if isinstance(self._kv.get(key), list):
            try:
                return self._kv[key][int(index)]
            except IndexError:
                return None
        return None


if __name__ == '__main__':
    logger = logging.getLogger('redis')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    Server().run()
