import network
from Tkinter import *
from random import *


root=Tk()


frame=Frame()
frame.pack()

canvas=Canvas(frame,width=500,height=500)
canvas.pack()


objects=[]
player=None


class ball:
	def __init__(self):
		objects.append(self)
		self.id=canvas.create_oval(10,10,100,100,fill="blue")

	def update(self):
		canvas.move(self.id,2,2)
		


class Player:

	moveDir=[0,0]

	def __init__(self):
		objects.append(self)
		self.id=canvas.create_rectangle(10,10,100,100,fill="blue")

	def update(self):
		canvas.move(self.id,self.moveDir[0],-self.moveDir[1])
		pass
		# canvas.move(self.id,2,2)
		


def restart():
	global player
	print 'restarting'
	ball()
	player=	Player()




def update():

	for obj in objects:
		obj.update()

	root.after(10,update)


def onclick(event):
	print event.keysym
	player.moveDir={"w":[0,1],"a":[-1,0],"s":[0,-1],"d":[1,0]}[event.keysym]


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