#!/usr/bin/python3

import speech_recognition as sr
import subprocess
from multiprocessing import Process, Pipe

a, b = Pipe()

def my_rec():
  cmd = 'arecord -N -D default:CARD=webcam -f S32_LE -r 44100 -t wav'.split(' ')
  r = sr.Recognizer()
  try:
      subprocess.run(cmd, timeout=5, stdout=subprocess.PIPE)
  except subprocess.TimeoutExpired as ex:
      source = sr.AudioData(ex.output, sample_rate=44100, sample_width=4)
      text = r.recognize_google(source, language='ru')
      b.send(text)

if __name__ == "__main__":
    while True:
        p = Process(target=my_rec)
        p.start()
        print(a.recv())
        p.join()


