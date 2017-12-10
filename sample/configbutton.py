import tkinter as tk
from .lover import main_loop
import threading
from .config_bbox import main

class ConfigButton:
  __slots__ = ['button', 'name', 'thread', 'gamebuttons']
  def __init__(self, button, buttonName, gamebuttons):
    self.button = button
    self.button.bind('<Button-1>', self.config)
    self.name = buttonName
    self.button['text'] = self.name.capitalize()
    self.thread = None
    self.gamebuttons = gamebuttons

  def config(self, event):
    for x in self.gamebuttons:
      x.stop()
    main()
