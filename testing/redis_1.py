import redis
import time

r = redis.Redis(host='localhost', port=6379)


print("redis1 : ", int(r.get('a')))
time.sleep(0.5)
r.set('a', 4)

