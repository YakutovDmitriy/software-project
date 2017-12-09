import pyscreenshot as grabber
from PIL import Image
import numpy as np
from tools import arr2pic, pic2arr, bool_pic


def config_bbox():
  default = (223, 195, 543, 517)
  red_pic = Image.open('pics/importants/red.png')
  red = pic2arr(red_pic)[0,0,:3]
  
  im = grabber.grab()
  im.save('pics/config_scrsht.png')
  a = pic2arr(im)
  n, m, _ = a.shape
  good = np.zeros((n, m), dtype=bool)
  for i in range(n):
    for j in range(m):
      if np.array_equal(a[i,j], red):
        good[i, j] = True
  bool_pic(good).save('pics/conf_bool.png')
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
          assert bbox == None
          bbox = (miny, minx, maxy, (5 * maxx + 4 * minx) // 9)
  assert bbox != None, 'you should launch confix_bbox when the circle is almost red'
  print("bbox is", bbox)
  grabber.grab(bbox).save('pics/X.png')
  return bbox

if __name__ == '__main__':
  bbox = config_bbox()
  with open('bbox/bbox.cfg', 'w') as b:
    print(bbox, file=b)
