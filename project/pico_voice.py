import struct
import pyaudio
import pvporcupine
import threading
import time
from time import sleep
from tkinter import  *

porcupine = None
pa = None
audio_stream = None


pa = pyaudio.PyAudio()

def pico():
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
            # print(keyword_index)
            if not keyword_index :
                # print("engine start")
                # print(time.time()-ss)
                audio_stream.close()
                return "engine start"

    # finally:
    #     if porcupine is not None:
    #         porcupine.delete()
    #
    #     if audio_stream is not None:
    #         audio_stream.close()
    #
    #     if pa is not None:
    #             pa.terminate()


def GUI():

    app = Tk()
    app.geometry('400x600')
    plabel = Label(master=app, text=pico())

    plabel.pack()
    app.mainloop()

#
# t1=threading.Thread(target=por1)
# t1.start()

GUI()