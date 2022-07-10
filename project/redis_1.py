import redis
import time

r = redis.Redis(host='localhost', port=6379)
data = [9]*1000
s = time.time()
data = bytes(data)
r.set(1, data)
print(time.time()-s)