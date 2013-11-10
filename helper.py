from Tkinter import *
from math import *
from PIL import ImageTk

# ===== Initialised empty, Updated by mainfile ===== #
objects=[]
bullets=[]
canvas=None
root=None

# ===== Player: the square, controlled by the user ===== #
class Player:
	def __init__(self):
		self.deltaX=[0,0]
	
		objects.append(self)
		photoimage = ImageTk.PhotoImage(file="graphics/player1.png")

		#pil has a bug in it, dont delete this line
		self.photoimage=photoimage

		self.width=photoimage.width()
		self.height=photoimage.height()

		self.id=canvas.create_image(101, 101, image=photoimage)
		# canvas.create_rectangle(200,200,300,300,fill="blue")

		# print(canvas.coords(self.id))

	def update(self):

		self.position=canvas.coords(self.id)
		self.position=[self.position[0]-self.width/2,self.position[1]-self.height/2,self.width/2+self.position[0],self.height/2+self.position[1]]

		# return

		if (self.position[2] >= 500) or (self.position[0] <= 0):
			self.deltaX[0]*=-1
		if (self.position[3] >= 500) or (self.position[1] <= 0):
			self.deltaX[1]*=-1

		# print self.position
		canvas.move(self.id,self.deltaX[0], self.deltaX[1])
		
# ===== Opponent: the opponent of Player ===== #
class Opponent:
	def __init__(self):
		self.deltaX=[0,0]
	
		objects.append(self)
		self.id=canvas.create_rectangle(200,200,300,300)#,fill="blue")
	
	def update(self):
		pass

# ===== Bullets are shot by the square ===== #
class Bullet:
	speed=10

	def __init__(self, pointer): # pointer refers to position of mouse pointer
		objects.append(self)
		bullets.append(self)
		
		playerPos=[(player.position[2]+player.position[0])/2, (player.position[3]+player.position[1])/2] # Shoot from the center
		direction=[pointer[0]-playerPos[0], pointer[1]-playerPos[1]] # Direction vector along which bullet will travel
		self.deltaX=vecScale(direction, self.speed)

		#self.id=canvas.create_line(playerPos, pointer, fill="red", dash=(4,4))
		self.id=canvas.create_oval(playerPos[0]-10,playerPos[1]+10,playerPos[0]+10,playerPos[1]-10, fill="red")
		root.after(1000, self.vanish)
		
	def vanish(self):
		canvas.delete(self.id)

		# These are called more than once for some reason
		if self in objects:
			objects.remove(self)
		if self in bullets:
			bullets.remove(self)

		del self
	
	def update(self):
		if self in objects:
			canvas.move(self.id,self.deltaX[0], self.deltaX[1])

def gfxInit():
	global player
	global opponent
	print 'restarting'
	canvas.delete(ALL)

	while len(objects):
		del objects[0]
	
	player=Player()
	opponent=Opponent()


def onKey(event):
	if event.keysym == "r":
		gfxInit()
	if event.keysym == "b":
		print "DEBUG DATA:"
		print "Player coords: ", canvas.coords(player.id)
		print "Player move vector: ", player.deltaX, " speed=", vecMagnitude(player.deltaX)
	if event.keysym == "x":
		player.deltaX=[0,0]
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
	
# Find magnitude of vector of size n
def vecMagnitude(vector):
	sq_sum=0
	for component in vector:
		sq_sum+=component**2
	return sqrt(sq_sum)

# Scale vector to size
def vecScale(vector, size):
	magnitude=vecMagnitude(vector)
	for count, component in enumerate(vector):
		vector[count]=component/magnitude
		vector[count]*=size
	return vector

if __name__ == '__main__':
	import mainfile
