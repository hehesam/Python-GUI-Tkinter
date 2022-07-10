import redis
import time

r = redis.Redis(host='localhost', port=6379)

while 1 :
    s = time.time()

    ss = int(r.get("engine start"))
    tt = int(r.get("engine stop"))
    if ss or tt :
        print("start : ",ss)
        print("stop : ",tt)

        time.sleep(1)

    print(time.time()-s)