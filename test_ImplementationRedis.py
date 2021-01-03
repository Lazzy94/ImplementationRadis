from unittest import TestCase
from ImplementationRedis import Server
from parameterized import parameterized
import pytest
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
        ('1', 1),
        (' 2', 2),
        ('test', 'test')
    ])
    def test_keys(self, key, value):
        self.server._kv[key] = value
        self.assertEqual(self.server.keys(), [key])

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
        ('1', 1, 5),
        (' 2', 2, 10),
        ('test', 'test', 15)
    ])
    def test_expire(self, key, value, ttl):
        self.server._kv[key] = value
        self.server.expire(key, ttl)
        time.sleep(ttl + 1)
        self.assertEqual(self.server._kv.get(key), None)

    # def test_connection_handler(self, con, address):
    #     self.server.connection_handler(con, address)
#TODO не понимаю как передать в тест параметры
    @parameterized.expand([
        ('set 1 1')
    ])
    def test_get_response(self, data):
        self.server.command = data[0, 1, 2].upper()
        self.assertEqual(self.server._commands[self.server.command](*data[4:]), None)
