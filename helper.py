from Tkinter import *
#updated by mainfile
objects=[]
canvas=None


class Player:

	#this runs when Player() is called
	def __init__(self):

		self.moveDir=[0,0]
	
		objects.append(self)
		self.id=canvas.create_rectangle(10,10,100,100,fill="blue")

	def update(self):
		canvas.move(self.id,self.moveDir[0],-self.moveDir[1])
		


def restart():
	global player
	global Ball
	print 'restarting'
	canvas.delete(ALL)
	
	player=Player()




def update():

	for obj in objects:
		obj.update()

	root.after(10,update)


def onclick(event):
	print event.keysym
	newMovedir={"w":[0,1],"a":[-1,0],"s":[0,-1],"d":[1,0]}[event.keysym]
	player.moveDir[0]+=newMovedir[0]
	player.moveDir[1]+=newMovedir[1]




if __name__ == '__main__':
	import mainfile