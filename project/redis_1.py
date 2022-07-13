import redis
import time

r = redis.Redis(host='localhost', port=6379)
# data = [9]*1000
# s = time.time()
# data = bytes(data)
# r.set(1, data)
# time.sleep(5)
# r.get(1)

print("redis1 : ", int(r.get('a')))
time.sleep(0.5)
r.set('a', 4)

