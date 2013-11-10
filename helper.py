from Tkinter import *
from math import *
from PIL import ImageTk

# ===== Initialised empty, Updated by mainfile ===== #
objects=[]
bullets=[]
opponentBullets=[]
bulletsToStopSending=[]
canvas=None
root=None
playerShot=None

# ===== Player: the square, controlled by the user ===== #
class Player:
	radius=50 # Radius of sprite is 50
	lives=5
	
	def __init__(self):
		self.deltaX=[0,0]
	
		objects.append(self)
		photoimage = ImageTk.PhotoImage(file="graphics/player1.png")

		# PIL has a bug in it, dont delete this line
		self.photoimage=photoimage

		self.id=canvas.create_image(250, 250, image=photoimage)

	def update(self):
		self.position=canvas.coords(self.id)
		
		# ===== Edge detection ===== #
		if (self.position[0] >= 450) or (self.position[0] <= 50):
			self.deltaX[0]*=-1
		if (self.position[1] >= 450) or (self.position[1] <= 50):
			self.deltaX[1]*=-1
			
		# ===== Hit detection (by bullet) ===== #
		for bullet in opponentBullets:
			edges=canvas.coords(bullet.id)
			bulletpos=[(edges[0]+edges[2])/2, (edges[1]+edges[3])/2]
			distance=[bulletpos[0]-self.position[0], bulletpos[1]-self.position[1]]
			if (5+self.radius)>=vecMagnitude(distance): # If the player is hit, -1
				self.lives-=1
				canvas.delete(bullet)
				bulletsToStopSending.append(bullet.uuid)
				# opponentBullets.remove(bullet)
				# send bullet back to opponent
		
		# ===== Limit speed to 10 ===== #
		if vecMagnitude(self.deltaX)>10:
			vecScale(self.deltaX, 10)

		canvas.move(self.id,self.deltaX[0], self.deltaX[1])
		
# ===== Opponent: the opponent of Player ===== #
class Opponent:
	radius=50
	
	def __init__(self):
		self.deltaX=[0,0]
	
		objects.append(self)

		photoimage = ImageTk.PhotoImage(file="graphics/player2.png")

		#pil has a bug in it, dont delete this line
		self.photoimage=photoimage

		self.width=photoimage.width()
		self.height=photoimage.height()

		self.id=canvas.create_image(100, 100, image=photoimage)
	
	def update(self):
		pass
	
# ===== Bullets are shot by the square ===== #
class Bullet:
	speed=10
	radius=5

	def __init__(self, pointer): # pointer refers to position of mouse pointer
		objects.append(self)
		bullets.append(self)
		
		direction=[pointer[0]-player.position[0], pointer[1]-player.position[1]] # Direction vector along which bullet will travel
		self.deltaX=vecScale(direction, self.speed)

		self.id=canvas.create_oval(player.position[0]-5,player.position[1]+5,player.position[0]+5,player.position[1]-5, fill="red")
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
		edges=canvas.coords(self.id)
		self.position=[(edges[0]+edges[2])/2, (edges[1]+edges[3])/2]
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
