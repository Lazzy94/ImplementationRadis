from unittest import TestCase
from ImplementationRedis import Server
from parameterized import parameterized
import time


class TestServer(TestCase):
    def setUp(self):
        self.server = Server()

    # @parameterized.expand([
    #     ('1', 1),
    #     (' 2', 2),
    #     ('test', 'test')
    # ])
    # def test_get(self, key, value):
    #     self.server._kv[key] = value
    #     assert self.server.get(key) == value
    #
    # @parameterized.expand([
    #     ('1', 1),
    #     (' 2', 2),
    #     ('test', 'test')
    # ])
    # def test_set(self, key, value):
    #     self.server.set(key, value)
    #     self.assertEqual(self.server._kv[key], value)
    #
    # @parameterized.expand([
    #     ({'pushkin1': 1,
    #       'pushkin2': 2,
    #       'blok1': 1}, 'pushkin')
    # ])
    # def test_keys(self, kvs, pattern):
    #     self.server._kv = kvs
    #     self.assertEqual(self.server.keys(pattern), ['pushkin1', 'pushkin2'])
    #
    # @parameterized.expand([
    #     ('1', 1),
    #     (' 2', 2),
    #     ('test', 'test')
    # ])
    # def test_delete(self, key, value):
    #     self.server._kv[key] = value
    #     self.server.delete(key)
    #     self.assertEqual(self.server._kv.get(key), None)
    #
    # @parameterized.expand([
    #     ('1', 1),
    #     (' 2', 2),
    #     ('test', 'test')
    # ])
    # def test_flush(self, key, value):
    #     self.server._kv[key] = value
    #     self.server.flush()
    #     self.assertEqual(self.server._kv, {})
    #
    # @parameterized.expand([
    #     ('1', 1, 2),
    #     (' 2', 2, 5),
    #     ('test', 'test', 10)
    # ])
    # def test_expire(self, key, value, ttl):
    #     self.server._kv[key] = value
    #     self.server.expire(key, ttl)
    #     time.sleep(ttl + 1)
    #     self.assertEqual(self.server._kv.get(key), None)
    #
    # @parameterized.expand([
    #     (['SET', '1', '1'], '1', {}),
    #     (['GET', '1'], '1', {'1': '1'}),
    #     (['KEYS', 'pushkin'], ['pushkin1', 'pushkin2'], {'pushkin1': 1,
    #                                                      'pushkin2': 2,
    #                                                      'blok1': 1})
    # ])
    # def test_get_response(self, data, response, kvs):
    #     self.server._kv = kvs
    #     self.assertEqual(self.server.get_response(data), response)

    # @parameterized.expand([
    #     ('odin', '1', '1'),
    #     (' dwa', '2', '2'),
    #     ('tree', '3', '3')
    # ])
    # def test_hset(self, key, field, value):
    #     self.server._kv.setdefault(key, {})
    #     self.assertEqual(self.server._kv[key][field], value)
    #
    # @parameterized.expand([
    #     ('1', '1'),
    #     (' 2', '2'),
    #     ('3', '3')
    # ])
    # def test_hget(self, k, field):
    #     self.server._kv[k] = [field]
    #     assert self.server._kv[k].get(field)

    @parameterized.expand([
        ('odin', 1, '1'),
        (' dwa', 2, '2'),
        ('tree', 3, '3')
    ])
    def test_lset(self, key, index, value):
        self.server._kv.setdefault(key, [])
        self.assertEqual(self.server._kv[key][index], value)

    def test_rpush(self):
        self.fail()

    def test_lpush(self):
        self.fail()

    def test_lrange(self):
        self.fail()
