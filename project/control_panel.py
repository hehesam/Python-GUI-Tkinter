import subprocess
import time
import redis
import threading


def start_voice():
    subprocess.run(
        ["gnome-terminal", "--", "sh", "-c", "python3 pico_voice.py", "&"])  # show the terminal "gnome-terminal", "--",


r = redis.Redis(host='localhost', port=6379)
while 1 :
    time.sleep(0.1)
    if int (r.get("start pico process")) == 1:
        voice_thread = threading.Thread(target=start_voice)
        r.set("start pico voice", 0)
