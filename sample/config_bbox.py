from .tools import pic2arr, bool_pic, in_files, in_temps
import numpy as np
from PIL import Image
import pyscreenshot as grabber
import sys


def config_bbox():
  red_pic = Image.open(in_files('red.png'))
  red = pic2arr(red_pic)[0,0,:3]

  im = grabber.grab()
  im.save(in_temps('config_scrsht.png'))
  a = pic2arr(im)
  n, m, _ = a.shape
  good = np.zeros((n, m), dtype=bool)
  for i in range(n):
    for j in range(m):
      if np.array_equal(a[i,j], red):
        good[i, j] = True
  bool_pic(good).save(in_temps('conf_bool.png'))
  bbox = None
  used = np.zeros((n, m), dtype=bool)
  for i in range(n):
    for j in range(m):
      if good[i, j] and not used[i, j]:
        q = [(i, j)]
        used[i, j] = True
        head = 0
        while head < len(q):
          x, y = q[head]
          head += 1
          for dx, dy in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            xx, yy = x + dx, y + dy
            if good[xx, yy] and not used[xx, yy]:
              q.append((xx, yy))
              used[xx, yy] = True
        q = np.array(q)
        minx, maxx = q[:,0].min(), q[:,0].max()
        miny, maxy = q[:,1].min(), q[:,1].max()
        if maxx - minx > 270 and maxy - miny > 270:
          assert bbox is None
          bbox = (miny, minx, maxy, (5 * maxx + 4 * minx) // 9)
  assert bbox != None, 'you should launch confix_bbox when the circle is almost red'
  print("bbox is", bbox, file=sys.stderr)
  grabber.grab(bbox).save(in_temps('X.png'))
  return bbox


def main():
  bbox = config_bbox()
  with open(in_files('bbox.cfg'), 'w') as b:
    print(bbox, file=b)


if __name__ == '__main__':
  main()
