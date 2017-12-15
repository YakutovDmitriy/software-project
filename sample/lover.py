from .songsdb import SongsDB
from .templategrabber import TemplateGrabber
from .tools import type_keyboard, in_files
import glob
import sys
import tkinter as tk


def main_loop(break_event=None, type_answer=False, text_field=None, get_wait_time=None):
  if get_wait_time is None:
    get_wait_time = lambda: random.randint(3, 7)
  print('start main loop', file=sys.stderr)
  last_templates = []
  max_size = 5
  with open(in_files('bbox.cfg')) as cfg:
    bbox = eval(cfg.readline())
    click = (bbox[2] + 20, (bbox[1] + bbox[3]) // 2)
  grabber = TemplateGrabber(bbox)
  if not (break_event is None) and break_event.is_set():
    return
  with open(in_files('db.txt')) as dbf:
    db = SongsDB(dbf)
  while True:
    if not (break_event is None) and break_event.is_set():
      return
    template = grabber.grab_template()
    print('template is %r' % template, file=sys.stderr)
    if not (template is None) and not (template in last_templates):
      did = False
      names = []
      for name in db.get_songs(template):
        if not did:
          print('-------------------------', file=sys.stderr)
          if text_field != None:
            text_field.config(state=tk.NORMAL)
            text_field.delete(1.0, tk.END)
          did = True
        print(name, file=sys.stderr)
        if text_field != None:
          text_field.insert(tk.END, name + '\n')
        names.append(name)
      if text_field != None:
        text_field.config(state=tk.DISABLED)
      if not (break_event is None) and break_event.is_set():
        break
      if len(names) > 0 and type_answer:
        type_keyboard(names, click, get_wait_time())
    if not (break_event is None) and break_event.is_set():
      return
    if template != None:
      if template in last_templates:
        last_templates.remove(template)
      last_templates.append(template)
      if len(last_templates) > max_size:
        last_templates.pop(0)


if __name__ == '__main__':
  main_loop()
