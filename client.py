import redis

client = redis.Redis(host='127.0.0.1', port=31337)
client.set(1, 1)
client.set(2, 2)
print(client.get(1))
print(client.get(2))
#TODO не работает метод KEYS
print(client.keys(str('*'))
