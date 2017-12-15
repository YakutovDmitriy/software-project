import tkinter as tk
from .configbutton import ConfigButton
from .gamebutton import GameButton
import random
import sys


def description():
  return """Hi guys.

This is bot for songclash game.
It can help you to guess songs or guess them without your involvement.

This bot can work in background, but game webpage must be visible.

Have a nice game!
"""


def main():
  root = tk.Tk()
  shape = (300, 550)
  root.geometry('%dx%d' % shape)
  root.title('Song lover')

  frame = tk.Frame(root)
  frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
  tk.Grid.rowconfigure(root, 0, weight=1)
  tk.Grid.columnconfigure(root, 0, weight=1)
  frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
  grid = tk.Frame(frame)
  grid.grid(sticky=tk.N + tk.S + tk.E + tk.W, column=0, row=4, columnspan=2)
  tk.Grid.rowconfigure(frame, 3, weight=1)
  tk.Grid.columnconfigure(frame, 0, weight=1)

  text_field = tk.Text(frame)
  text_field.grid(row=4, sticky=tk.N + tk.S + tk.E + tk.W)
  text_field.insert(tk.END, description())
  text_field.config(state=tk.DISABLED)

  waiter = tk.Scale(frame, label='Wait before answer (in seconds)',
        length=int(shape[1] * 0.9), orient=tk.HORIZONTAL, from_=3.0, to=20.0)
  waiter.grid(row=1, sticky=tk.N + tk.S + tk.E + tk.W)

  def get_wait_time(waiter):
    left = max(0, waiter.get() - 0.5)
    right = left + 1
    res = random.uniform(left, right)
    print('res is %r, type is %r' % (res, type(res)), file=sys.stderr)
    return

  typeButton = GameButton(button=tk.Button(frame),
        buttonName='type answers', type_answer=True, text_field=text_field,
        get_wait_time=lambda: get_wait_time(waiter))
  typeButton.button.grid(row=0, sticky=tk.N + tk.S + tk.E + tk.W)

  tipsButton = GameButton(button=tk.Button(frame),
        buttonName='show tips', type_answer=False, text_field=text_field)
  tipsButton.button.grid(row=2, sticky=tk.N + tk.S + tk.E + tk.W)

  GameButton.exclusive(typeButton, tipsButton)

  confButton = ConfigButton(button=tk.Button(frame),
        buttonName='find circle', gamebuttons=(typeButton, tipsButton))
  confButton.button.grid(row=3, sticky=tk.N + tk.S + tk.E + tk.W)

  def stopall(root, *games):
    for x in games:
      x.stop_thread()
    root.destroy()
  root.protocol("WM_DELETE_WINDOW", lambda: stopall(root, typeButton, tipsButton))
  root.mainloop()
