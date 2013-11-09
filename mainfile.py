import network
from network import *
import helper
from helper import *

from Tkinter import *
from random import *


root=Tk()


frame=Frame()
frame.grid(row=0,column=0)

canvas=Canvas(frame,width=500,height=500)
canvas.grid(row=0,column=0)

lowerFrame=Frame(width=root.winfo_screenwidth())
lowerFrame.grid(row=1,column=0)

objects=[]
player=None


helper.objects=objects
helper.canvas=canvas


network.lowerFrame=lowerFrame
network.root=root


def update():


	for obj in objects:

		obj.update()

	root.after(10,update)


# ===== Keybinding ===== #
# w,a,s,d -> move
# r -> restart
# ESC,q -> quit
# b -> debug
root.bind("w", onclick)
root.bind("a", onclick)
root.bind("s", onclick)
root.bind("d", onclick)
root.bind("r", onclick)
root.bind("b", onclick)
root.bind("q", exit)

root.bind("<Escape>", exit)

Button(lowerFrame, text="Restart",command=gfxInit).grid(row=1,column=0)

#start update loop
root.after(10,update)

# ===== Init functions ===== #
gfxInit()
networkInit()

root.mainloop()


