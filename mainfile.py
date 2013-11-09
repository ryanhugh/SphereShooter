import network
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


def update():
	for obj in objects:
		obj.update()

	root.after(10,update)


#bind controls
root.bind("w", onclick)
root.bind("a", onclick)
root.bind("s", onclick)
root.bind("d", onclick)



Button(frame, text="Restart",command=restart).pack()

#start update loop
root.after(10,update)

#make game stuff
restart()

#exit when u click esc
root.bind("<Escape>", exit)


root.mainloop()


