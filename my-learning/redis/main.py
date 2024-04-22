import random
import redis


S = 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>!@#$%^&*()1234567890-=qwertyuiop[]asdfghjkl;zxcvbnm,./'


redis_client = redis.Redis(host='localhost', port=6379, db=0)
print(redis_client.set('one', 1))
print(redis_client.get('one'))
print(redis_client.incr('one'))
print(redis_client.incrby('one', 10))
print(redis_client.delete('one'))
print(redis_client.delete('one'))
print(redis_client.delete('one'))
for i in range(100_000):
    redis_client.set(str(random.sample(S, random.randint(1, 30))), str(random.sample(S, random.randint(1, 30))))
print(len(redis_client.keys()))
redis_client.flushall()
redis_client.close()
# print(redis_client.)
# print(redis_client.values())
