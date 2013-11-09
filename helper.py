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
		if (canvas.coords(self.id)[0] >= 400) or (canvas.coords(self.id)[0] <= 0):
			self.moveDir[0]*=-1
		if (canvas.coords(self.id)[1] >= 400) or (canvas.coords(self.id)[1] <= 0):
			self.moveDir[1]*=-1
			
		canvas.move(self.id,self.moveDir[0], self.moveDir[1])
		


def init():
	global player
	print 'restarting'
	canvas.delete(ALL)
	for i in range(len(objects)):
		del objects[i]
	
	player=Player()


def onclick(event):
	if event.keysym == "r":
		init()
	if event.keysym == "b":
		print "DEBUG DATA:"
		print "Player coords: ", canvas.coords(player.id)
		print "Player move vector: ", player.moveDir
	elif event.keysym in ["w","a","s","d"]:
		newMovedir={"w":[0,-1],"a":[-1,0],"s":[0,1],"d":[1,0]}[event.keysym]
		player.moveDir[0]+=newMovedir[0]
		player.moveDir[1]+=newMovedir[1]


if __name__ == '__main__':
	import mainfile
