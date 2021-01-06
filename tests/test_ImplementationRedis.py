from unittest import TestCase
from ImplementationRedis import Server
from parameterized import parameterized
import time


class TestServer(TestCase):
    def setUp(self):
        self.server = Server()

    @parameterized.expand([
        ('1', 1),
        (' 2', 2),
        ('test', 'test')
    ])
    def test_get(self, key, value):
        self.server._kv[key] = value
        assert self.server.get(key) == value

    @parameterized.expand([
        ('1', 1),
        (' 2', 2),
        ('test', 'test')
    ])
    def test_set(self, key, value):
        self.server.set(key, value)
        self.assertEqual(self.server._kv[key], value)

    @parameterized.expand([
        ({'pushkin1': 1,
          'pushkin2': 2,
          'blok1': 1}, 'pushkin')
    ])
    def test_keys(self, kvs, pattern):
        self.server._kv = kvs
        self.assertEqual(self.server.keys(pattern), ['pushkin1', 'pushkin2'])

    @parameterized.expand([
        ('1', 1),
        (' 2', 2),
        ('test', 'test')
    ])
    def test_delete(self, key, value):
        self.server._kv[key] = value
        self.server.delete(key)
        self.assertEqual(self.server._kv.get(key), None)

    @parameterized.expand([
        ('1', 1),
        (' 2', 2),
        ('test', 'test')
    ])
    def test_flush(self, key, value):
        self.server._kv[key] = value
        self.server.flush()
        self.assertEqual(self.server._kv, {})

    @parameterized.expand([
        ('1', 1, 2),
        (' 2', 2, 5),
        ('test', 'test', 10)
    ])
    def test_expire(self, key, value, ttl):
        self.server._kv[key] = value
        self.server.expire(key, ttl)
        time.sleep(ttl + 1)
        self.assertEqual(self.server._kv.get(key), None)

    @parameterized.expand([
        (['SET', '1', '1'], '1', {}),
        (['GET', '1'], '1', {'1': '1'}),
        (['KEYS', 'pushkin'], ['pushkin1', 'pushkin2'], {'pushkin1': 1,
                                                         'pushkin2': 2,
                                                         'blok1': 1})
    ])
    def test_get_response(self, data, response, kvs):
        self.server._kv = kvs
        self.assertEqual(self.server.get_response(data), response)

    @parameterized.expand([
        ('one', '1', '1'),
        (' two', '2', '2'),
        ('three', '3', '3')
    ])
    def test_hset(self, key, field, value):
        self.server.hset(key, field, value)
        self.assertEqual(self.server._kv[key][field], value)

    @parameterized.expand([
        ('1', '1', '1'),
        (' 2', '2', '2'),
        ('3', '3', '3')
    ])
    def test_hget(self, key, field, value):
        self.server._kv.setdefault(key, {field: value})
        self.assertEqual(self.server.hget(key, field), value)

    @parameterized.expand([
        ('my_list', 1, '1'),
        ('my_list', 1, '2'),
        ('my_list', 1, '3')])
    def test_lset(self, key, index, value):
        self.server.rpush('my_list', '4')
        self.server.rpush('my_list', '5')
        self.server.lset(key, index, value)
        self.assertEqual(self.server._kv[key][index], value)

    @parameterized.expand([
        ('my_list', '1', '2'),
        ('my_list', '2', '3'),
        ('my_list', '3', '4')])
    def test_rpush(self, key, *value):
        self.server.rpush(key, *value)
        self.assertEqual(self.server._kv[key], list(value))

    @parameterized.expand([
        ('my_list', '2', '1'),
        ('my_list', '3', '2'),
        ('my_list', '4', '3')])
    def test_lpush(self, key, *value):
        self.server.lpush(key, *value)
        self.assertEqual(self.server._kv[key], list(reversed(value)))

    @parameterized.expand([
        ('my_list', 0, -1),
        ('my_list', 1, 3),
        ('my_list', 0, 3)])
    def test_lrange(self, key, start, end):
        self.server.rpush('my_list', '1', '2', '3', '4')
        self.server.lrange(key, start, end)
        self.assertEqual(self.server._kv[key][start:end], self.server._kv[key][start:end])

    @parameterized.expand([
        ('my_list', 0),
        ('my_list', 1),
        ('my_list', 2)])
    def test_lindex(self, key, index):
        self.server.rpush('my_list', '1', '2', '3', '4')
        self.server.lindex(key, index)
        self.assertEqual(self.server._kv[key][index], self.server._kv[key][index])
