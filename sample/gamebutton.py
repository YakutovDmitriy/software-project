import tkinter as tk
from .lover import main_loop
import threading

class GameButton:
  __slots__ = ['button', 'name', 'type_answer', 'thread', 'exs', 'break_event', 'state', 'text_field']
  def __init__(self, button, buttonName, type_answer, text_field):
    self.button = button
    self.button.bind('<Button-1>', self.flip)
    self.text_field = text_field
    self.name = buttonName.lower()
    self.type_answer = type_answer
    self.thread = None
    self.exs = []
    self.break_event = threading.Event()
    self.state = None
    self.stop()

  def stop(self):
    self.stop_thread()
    self.button['text'] = 'Start %s' % self.name
    self.state = 'stop'

  def start(self):
    for gb in self.exs:
      gb.stop()
    self.thread = threading.Thread(target=main_loop,
          name='game', args=(self.break_event, self.type_answer, self.text_field))
    self.thread.start()
    self.button['text'] = 'Stop %s' % self.name
    self.state = 'start'

  def flip(self, event):
    print('flip')
    if self.state == 'stop':
      self.start()
    else:
      self.stop()

  def stop_thread(self):
    if self.thread != None and self.thread.is_alive():
      self.break_event.set()
      self.thread.join()
      self.break_event.clear()
    self.thread = None

  def exclusive(gb1, gb2):
    gb1.exs.append(gb2)
    gb2.exs.append(gb1)
