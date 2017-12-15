import pyscreenshot
import numpy as np
from .tools import pic2arr


class TemplateGrabber:

  __slots__ = ['bbox', 'max_dist_pix', 'max_hei_pix']

  def __init__(self, boundingbox):
    self.bbox = boundingbox
    self.max_dist_pix = 5
    self.max_hei_pix = 3

  def grab_template(self):
    im = pyscreenshot.grab(bbox=self.bbox)
    # im.save(in_temps('working.png'))
    a = pic2arr(im)
    n, m = a.shape[0], a.shape[1]
    b = np.zeros((n, m))
    for i in range(n):
      for j in range(m):
        x, y, z = map(lambda q: 2 ** 8 - 1 - q, a[i, j].tolist())
        b[i, j] = float(x + y + z)
    white = b.min()
    good = np.zeros((n, m), dtype=bool)
    for i in range(n):
      for j in range(m):
        good[i, j] = b[i, j] == white
    answer = []
    for i in range(n):
      lastR, cur_length = -10**10, 0
      for j in range(m):
        if good[i, j]:
          L, R = j, j
          while R < m and good[i, R]:
            R += 1
          if R == m:
            return None
          for x in range(i, min(n, i + self.max_hei_pix + 1)):
            for y in range(L, min(m, R + 1)):
              good[x, y] = False
          if L - lastR <= self.max_dist_pix:
            cur_length += 1
          else:
            if cur_length > 0:
              answer.append(cur_length)
            cur_length = 1
          lastR = R
      if cur_length > 0:
        answer.append(cur_length)
    # if len(answer) > 9:
    #   bool_pic(good).save(in_temps('bool.png'))
    return answer
