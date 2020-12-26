from unittest import TestCase
from ImplementationRedis import Server
from parameterized import parameterized


class TestServer(TestCase):
    def setUp(self):
        self.server = Server()

    # def test_get_commands(self):
    #     self.fail()
    #
    # def test_connection_handler(self):
    #     self.fail()
    #
    # def test_run(self):
    #     self.fail()
    #
    # def test_get_response(self):
    #     self.fail()
    @parameterized.expand([
        ('name', 1, 1),
        ('key', 2, 2)])
    def test_get(self, key, value):
        self.server._kv[key] = value
        assert self.server.get(key) == value

    def test_set(self, key, value):
        self.server.set(key, value)
        self.assertEqual(self.server.get(key), value)
    #
    # def test_delete(self):
    #     self.fail()
    #
    # def test_keys(self):
    #     self.fail()
    #
    # def test_flush(self):
    #     self.fail()
    #
    # def test_expire(self):
    #     self.fail()

# class TestClient(TestCase):
#     def test_execute(self):
#         self.fail()
#
#     def test_get(self):
#         self.fail()
#
#     def test_set(self):
#         self.fail()
#
#     def test_delete(self):
#         self.fail()
#
#     def test_flush(self):
#         self.fail()
#
#     def test_keys(self):
#         self.fail()
