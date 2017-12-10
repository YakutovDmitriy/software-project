import tkinter as tk
from .gamebutton import GameButton
from .configbutton import ConfigButton


def main():
  root = tk.Tk()
  shape = (190, 81)
  root.geometry('%dx%d' % shape)
  root.title('Song lover')

  frame = tk.Frame(root)
  tk.Grid.rowconfigure(root, 0, weight=1)
  tk.Grid.columnconfigure(root, 0, weight=1)
  frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
  grid = tk.Frame(frame)
  grid.grid(sticky=tk.N + tk.S + tk.E + tk.W, column=0, row=3, columnspan=2)
  tk.Grid.rowconfigure(frame, 3, weight=1)
  tk.Grid.columnconfigure(frame, 0, weight=1)

  typeButton = GameButton(button=tk.Button(frame), 
        buttonName='type answers', type_answer=True)
  typeButton.button.grid(sticky=tk.N + tk.S + tk.E + tk.W, row=0)

  tipsButton = GameButton(button=tk.Button(frame), 
        buttonName='show tips', type_answer=False)
  tipsButton.button.grid(sticky=tk.N + tk.S + tk.E + tk.W, row=1)

  GameButton.exclusive(typeButton, tipsButton)

  confButton = ConfigButton(button=tk.Button(frame), 
        buttonName='find circle', gamebuttons=(typeButton, tipsButton))
  confButton.button.grid(sticky=tk.N + tk.S + tk.E + tk.W, row=2)

  def stopall(root, *games):
    for x in games:
      x.stop_thread()
    root.destroy()
  root.protocol("WM_DELETE_WINDOW", lambda: stopall(root, typeButton, tipsButton))
  root.mainloop()
