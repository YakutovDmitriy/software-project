import pyscreenshot as grabber
from PIL import Image
import numpy as np
import win32api
import win32con
import win32com.client as comclt
import time

def arr2pic(arr):
  return Image.fromarray(np.uint8(arr))

def pic2arr(pic):
  return np.array(pic)

def bool_pic(good):
  n, m = good.shape
  pic = np.zeros((n, m, 3))
  for i in range(n):
    for j in range(m):
      if good[i, j]:
        for x in range(3):
           pic[i,j,x] = 0
      else:
        for x in range(3):
          pic[i,j,x] = 255
  return arr2pic(pic)


wsh = comclt.Dispatch("WScript.Shell")
def type_keyboard(strs, coords=None, seconds_to_wait=None):
  if coords != None:
    x, y = coords
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
  if seconds_to_wait != None:
    time.sleep(seconds_to_wait)
  for s in strs:
    for ch in s.lower():
      wsh.SendKeys(ch)
    wsh.SendKeys('~')
    time.sleep(0.05)
