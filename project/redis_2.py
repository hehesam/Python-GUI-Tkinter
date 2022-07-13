# import redis
import time
#
# r = redis.Redis(host='localhost', port=6379)
#
# while 1 :
#     s = time.time()
#
#     ss = int(r.get("engine start"))
#     tt = int(r.get("engine stop"))
#     if ss or tt :
#         print("start : ",ss)
#         print("stop : ",tt)
#         time.sleep(1)
#
#     print(time.time()-s)

import subprocess
import os
import redis
r = redis.Redis(host='localhost', port=6379)
print(int(r.get('a')))

r.set('a', 1)
    run = os.system("python3 redis_1.py")


# subprocess.call([ "gnome-terminal", "--","sh", "-c", "python3 redis_1.py"], )

# subprocess.Popen(["python3","redis_1.py"],creationflags=subprocess.CREATE_NEW_CONSOLE)

# subprocess.call(['python3', 'redis_1.py'], shell=True)
# p = subprocess.run(['python3','redis_1.py'], shell=True)
# print("Hi",p.returncode)

time.sleep(1)
print(int(r.get('a')))
# subprocess.call(["gnome-terminal", "--", "sh", "-c", "python3 pico_voice.py"])
# print("hello "%run)
# time.sleep(2)
# while 1 :
#     print(1)