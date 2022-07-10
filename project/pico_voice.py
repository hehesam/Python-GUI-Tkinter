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
        keyword_paths = ['~/programs/python/python-GUI-tkinter/project/voice_pico/engine-start_en_linux_v2_1_0.ppn'])
        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        while True:
            ss = time.time()
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            r = redis.Redis(host='localhost', port=6379)
            if not keyword_index :
                r.set("engine start", 1)
                print("engine start")
                # print(time.time()-ss)
                # audio_stream.close()
            else :
                r.set("engine start", 0)


def stop():
    porcupine = pvporcupine.create(access_key='1Abqm0SPQtUR4iFUuBFEepTjGpDoD5RN8XrpjlbAVJp2nk8WSiyh/Q==',
                                   keyword_paths=[
                                       '~/programs/python/python-GUI-tkinter/project/voice_pico/engine-stop_en_linux_v2_1_0.ppn'])
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)

    while True:
        ss = time.time()
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        r = redis.Redis(host='localhost', port=6379)
        if not keyword_index:
            r.set("engine stop", 1)
            print("engine stop")
            # print(time.time()-ss)
            # audio_stream.close()
        else :
            r.set("engine stop", 0)


t1=threading.Thread(target=start)
t2=threading.Thread(target=stop)

t1.start()
t2.start()
# start()
