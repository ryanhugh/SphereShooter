from Tkinter import *
from math import *

# ===== Initialised empty, Updated by mainfile ===== #
objects=[]
canvas=None
root=None

# ===== Player: the square, controlled by the user ===== #
class Player:
	def __init__(self):
		self.deltaX=[0,0]
	
		objects.append(self)
		self.id=canvas.create_rectangle(200,200,300,300,fill="blue")

	def update(self):
		self.position=canvas.coords(self.id)
		if (self.position[2] >= 500) or (self.position[0] <= 0):
			self.deltaX[0]-=1.9*self.deltaX[0] # No longer a perfectly elastic collision
		if (self.position[3] >= 500) or (self.position[1] <= 0):
			self.deltaX[1]-=1.9*self.deltaX[1] # No longer a perfectly elastic collision
		
		canvas.move(self.id,self.deltaX[0], self.deltaX[1])
		
# ===== Opponent: the opponent of Player ===== #
class Opponent:
	def __init__(self):
		self.deltaX=[0,0]
	
		objects.append(self)
		self.id=canvas.create_rectangle(200,200,300,300,fill="blue")
	
	def update(self):
		pass

# ===== Bullets are shot by the square ===== #
class Bullet:
	def __init__(self, pointer): # pointer refers to position of mouse pointer
		objects.append(self)
		print objects
		print self in objects
		
		playerPos=[(player.position[2]+player.position[0])/2, (player.position[3]+player.position[1])/2] # Shoot from the center
		self.id=canvas.create_line(playerPos, pointer, fill="red", dash=(4,4))
		
	def vanish(self):
		canvas.delete(self.id)
		objects.remove(self)
	
	def update(self):
		root.after(100, self.vanish)

def gfxInit():
	global player
	global opponent
	print 'restarting'
	canvas.delete(ALL)
	for i in range(len(objects)):
		del objects[i]
	
	player=Player()
	opponent=Opponent()


def onKey(event):
	if event.keysym == "r":
		gfxInit()
	if event.keysym == "b":
		print "DEBUG DATA:"
		print "Player coords: ", canvas.coords(player.id)
		print "Player move vector: ", player.deltaX, " speed=", sqrt(player.deltaX[0]**2+player.deltaX[1]**2)
	elif event.keysym in ["w","a","s","d"]:
		deltaV={"w":[0,-1],"a":[-1,0],"s":[0,1],"d":[1,0]}[event.keysym]
		player.deltaX[0]+=deltaV[0]
		player.deltaX[1]+=deltaV[1]
	elif event.keysym in ["<Escape>", "q"]:
		exit()
	else: # This keypress shouldn't be handled
		return

def onClick(event):
	mouse=[event.x, event.y] # Coordinates of mouse at click
	playerShot=Bullet(mouse)
	print mouse

if __name__ == '__main__':
	import mainfile
