from Tkinter import *
from random import *


root=Tk()


frame=Frame()
frame.pack()

canvas=Canvas(frame,width=500,height=500)
canvas.pack()

def restart():
	print 'restarting'


Button(frame, text="Restart",command=restart).pack()

root.mainloop()