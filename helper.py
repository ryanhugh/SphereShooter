from Tkinter import *
from math import *
#updated by mainfile
objects=[]
canvas=None

class Player:

	#this runs when Player() is called
	def __init__(self):

		self.moveDir=[0,0]
	
		objects.append(self)
		self.id=canvas.create_rectangle(200,200,300,300,fill="blue")

	def update(self):
		if (canvas.coords(self.id)[2] >= 500) or (canvas.coords(self.id)[0] <= 0):
			self.moveDir[0]-=1.9*self.moveDir[0] # No longer a perfectly elastic collision
		if (canvas.coords(self.id)[3] >= 500) or (canvas.coords(self.id)[1] <= 0):
			self.moveDir[1]-=1.9*self.moveDir[1] # No longer a perfectly elastic collision
			
		canvas.move(self.id,self.moveDir[0], self.moveDir[1])

#class Bullet:
	

def gfxInit():
	global player
	print 'restarting'
	canvas.delete(ALL)
	for i in range(len(objects)):
		del objects[i]
	
	player=Player()


def onKey(event):
	if event.keysym == "r":
		gfxInit()
	if event.keysym == "b":
		print "DEBUG DATA:"
		print "Player coords: ", canvas.coords(player.id)
		print "Player move vector: ", player.moveDir, " speed=", sqrt(player.moveDir[0]**2+player.moveDir[1]**2)
	elif event.keysym in ["w","a","s","d"]:
		newMovedir={"w":[0,-1],"a":[-1,0],"s":[0,1],"d":[1,0]}[event.keysym]
		player.moveDir[0]+=newMovedir[0]
		player.moveDir[1]+=newMovedir[1]
	elif event.keysym in ["<Escape>", "q"]:
		exit()
	else: # This keypress shouldn't be handled
		return

def onClick(event):
	mouse=[event.x, event.y] # Coordinates of mouse at click
	print mouse

if __name__ == '__main__':
	import mainfile
