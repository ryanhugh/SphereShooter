from Tkinter import *
from random import*


root=Tk()


frame=Frame()
frame.pack()

canvas=Canvas(frame, bg="black",width=500,height=500)
canvas.pack()

clock=Label(frame, fg="white")
clock.pack()


root.mainloop()