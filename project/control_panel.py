import subprocess
import time
import redis
import threading


def start_voice():
    print("pico thread")
    subprocess.run(
        ["sh", "-c", "python3 pico_voice.py"])  # show the terminal "gnome-terminal", "--",

def start_unity():
    print("unity thread")
    subprocess.run(
        subprocess.call(["sh", "-c", "./unity_game2/rope.x86_64"]))

r = redis.Redis(host='localhost', port=6379)
r.set("start pico process", 0)
r.set("start unity process", 0)
# for i in range(999):
i = 0
while 1 :
    i += 1
    time.sleep(0.1)
    print("loop: ",i, int(r.get("start pico process")))
    if int (r.get("start pico process")) == 1:
        print("pico process started")
        voice_thread = threading.Thread(target=start_voice)
        voice_thread.start()
        r.set("start pico process", 0)

    if int(r.get("start unity process")) == 1:
        print("unity process started")
        unity_thread = threading.Thread(target=start_unity)
        unity_thread.start()
        r.set("start unity process", 0)
