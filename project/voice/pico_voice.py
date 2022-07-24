import struct
import pyaudio
import pvporcupine
import threading
import time
import redis
porcupine = None
pa = None
audio_stream = None


pa = pyaudio.PyAudio()

def start():
        porcupine = pvporcupine.create(access_key='1Abqm0SPQtUR4iFUuBFEepTjGpDoD5RN8XrpjlbAVJp2nk8WSiyh/Q==',
        keyword_paths = ['~/programs/python/python-GUI-tkinter/project/voice/engine-start_en_linux_v2_1_0.ppn'])
        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        r = redis.Redis(host='localhost', port=6379)
        r.set("end pico process", 0)

        while True:
            ss = time.time()
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if not keyword_index :
                r.set("engine start", 1)
                print("engine start")
                # print(time.time()-ss)
                # audio_stream.close()
            else :
                r.set("engine start", 0)

            if int(r.get("end pico process")) == 1:
                print("by")
                break


def stop():
    porcupine = pvporcupine.create(access_key='1Abqm0SPQtUR4iFUuBFEepTjGpDoD5RN8XrpjlbAVJp2nk8WSiyh/Q==',
                                   keyword_paths=[
                                       '~/programs/python/python-GUI-tkinter/project/voice/engine-stop_en_linux_v2_1_0.ppn'])
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)

    r = redis.Redis(host='localhost', port=6379)
    r.set("end pico process", 0)

    while True:
        ss = time.time()
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        if not keyword_index:
            r.set("engine stop", 1)
            print("engine stop")
            # print(time.time()-ss)
            # audio_stream.close()
        else :
            r.set("engine stop", 0)

        if int(r.get("end pico process")) == 1:
            print("by")
            time.sleep(1)
            break


t1=threading.Thread(target=start)
t2=threading.Thread(target=stop)

t1.start()
t2.start()
# start()
