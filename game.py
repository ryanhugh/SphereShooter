from Tkinter import *
from random import *


root=Tk()


frame=Frame()
frame.pack()

canvas=Canvas(frame,width=500,height=500)
canvas.pack()


objects=[]


class ball:
	def __init__(self):
		objects.append(self)
		self.id=canvas.create_oval(10,10,100,100,fill="blue")

	def update(self):
		canvas.move(self.id,2,2)
		


def restart():
	print 'restarting'
	ball()




def update():

	for obj in objects:
		obj.update()

	root.after(10,update)








Button(frame, text="Restart",command=restart).pack()

root.after(10,update)

restart()

root.bind("<Escape>", exit)


root.mainloop()