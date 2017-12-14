import pyscreenshot as grabber
from PIL import Image
import numpy as np
try:
  from .tools import arr2pic, pic2arr, bool_pic, type_keyboard, in_files, in_temps
except:
  from tools import arr2pic, pic2arr, bool_pic, type_keyboard, in_files, in_temps
import random
import os
import glob, sys
import tkinter as tk

def from_display(bbox):
  im = grabber.grab(bbox=bbox)
  # im.save(in_temps('working.png'))
  a = pic2arr(im)
  n, m = a.shape[0], a.shape[1]
  b = np.zeros((n, m))
  for i in range(n):
    for j in range(m):
      x, y, z = map(lambda q: 255 - q, a[i,j].tolist())
      b[i, j] = float(x + y + z)
  white = b.min()
  good = np.zeros((n, m), dtype=bool)
  for i in range(n):
    for j in range(m):
      good[i, j] = b[i, j] == white
  # bool_pic(good).save(in_temps('bool.png'))
  answer = []
  for i in range(n):
    lastR, curLen = -123, 0
    for j in range(m):
      if good[i, j]:
        L, R = j, j
        while R < m and good[i, R]:
          R += 1
        if R == m:
          return None
        for x in range(i - 1, min(n, i + 2)):
          for y in range(L, min(m, R + 1)):
            good[x, y] = False
        if L - lastR <= 5:
          curLen += 1
        else:
          if curLen > 0:
            answer.append(curLen)
          curLen = 1
        lastR = R
    if curLen > 0:
      answer.append(curLen)
  # if len(answer) > 9:
  #   bool_pic(good).save(in_temps('bool.png'))
  return answer

def load_db(db):
  def toword(s):
    return ''.join(filter(str.isalnum, s))
  res = []
  for line in db:
    line = line.strip()
    words = line.split()
    words = filter(lambda x: len(x) > 0, words)
    words = list(map(toword, words))
    res.append(words)
  return res

def from_db(db, template):
  for words in db:
    cur = list(map(len, words))
    if cur == template:
      yield ' '.join(words)

def main_loop(break_event=None, type_answer=False, text_field=None):
  print('start main loop')
  last_temps = []
  max_size = 5
  with open(in_files('bbox.cfg')) as cfg:
    bbox = eval(cfg.readline())
    click = (bbox[2] + 20, (bbox[1] + bbox[3]) // 2)
  if break_event != None and break_event.is_set():
    return
  with open(in_files('db.txt')) as dbf:
    db = load_db(dbf)
  if break_event != None and break_event.is_set():
    return
  while True:
    if break_event != None and break_event.is_set():
      return
    template = from_display(bbox)
    if template != None and not (template in last_temps):
      did = False
      names = []
      for name in from_db(db, template):
        if not did:
          print('-------------------------')
          if text_field != None:
            text_field.config(state=tk.NORMAL)
            text_field.delete(1.0, tk.END)
          did = True
        print(name)
        if text_field != None:
          text_field.insert(tk.END, name + '\n')
        names.append(name)
      if text_field != None:
        text_field.config(state=tk.DISABLED)
      if break_event != None and break_event.is_set():
        break
      if len(names) > 0 and type_answer: 
        secs = random.randint(3, 7)
        type_keyboard(names, click, secs)
    if break_event != None and break_event.is_set():
      return
    if template != None:
      if template in last_temps:
        last_temps.remove(template)
      last_temps.append(template)
      if len(last_temps) > max_size:
        last_temps.pop(0)
        
if __name__ == '__main__':
  main_loop()
