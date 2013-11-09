import network
from network import *
import helper
from helper import *

from Tkinter import *
from random import *


root=Tk()


frame=Frame()
frame.pack()

canvas=Canvas(frame,width=500,height=500)
canvas.pack()


objects=[]
player=None


helper.objects=objects
helper.canvas=canvas


network.frame=frame
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

Button(frame, text="Restart",command=init).pack()

#start update loop
root.after(10,update)

#make game stuff
init()

networkInit()


root.mainloop()


