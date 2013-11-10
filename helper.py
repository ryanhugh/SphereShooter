from Tkinter import *
from math import *
from PIL import ImageTk


# ===== Constants ===== #
CANVASWIDTH=1200
CANVASHEIGHT=650

PLAYERLIVES=20
CONTROLSENSITIVITY=.2

# ===== Initialized empty, Updated by mainfile ===== #
canvas=None
root=None
updateLivesLabel=None
restartfn=None


# ===== Important lists for this file ===== #
objects=[]
bullets=[]
opponentBullets=[]

# playerShot=None #this didn't do anything?

#keep track of bullets that hit so any network lag doesn't cause the same bullet to hit twice
bulletsThatHitMe=[]

#tell opponent to stop sending these bullets
bulletsToStopSending=[]

#keep track of pressed keys for smooth movement
pressedKeys={"w":False,"a":False,"s":False,"d":False}

# ===== Player: the square, controlled by the user ===== #
class Player:
	RADIUS=50
	MAXSPEED=10
	
	def __init__(self):
		self.deltaX=[0,0]
		self.lives=PLAYERLIVES
		photoimage = ImageTk.PhotoImage(file="graphics/player1.png")

		# PIL has a bug in it, don't delete this line
		self.photoimage=photoimage

		self.id=canvas.create_image(250, 250, image=photoimage)

		self.position=canvas.coords(self.id)

		# keep track of all objects for main update loop
		objects.append(self)

	def update(self):
		self.position=canvas.coords(self.id)
		
		# ===== Edge detection ===== #
		if (self.position[0] >= CANVASWIDTH-player.RADIUS) or (self.position[0] <= player.RADIUS):
			self.deltaX[0]*=-1
		if (self.position[1] >= CANVASHEIGHT-player.RADIUS) or (self.position[1] <= player.RADIUS):
			self.deltaX[1]*=-1
			
		# ===== Hit detection (by bullet) ===== #
		for bullet in opponentBullets:
			edges=canvas.coords(bullet.id)
			bulletpos=[(edges[0]+edges[2])/2, (edges[1]+edges[3])/2]
			distance=[bulletpos[0]-self.position[0], bulletpos[1]-self.position[1]]
			if (bullet.RADIUS+self.radius)>=vecMagnitude(distance): # If the player is hit, -1

				#if already hit that bullet, don't count it again (network lag)
				if bullet.uuid in bulletsThatHitMe:
					continue

				self.lives-=1
				updateLivesLabel()

				canvas.delete(bullet)

				# save to tell sender that you need to remove this bullet
				bulletsToStopSending.append(bullet.uuid)

				# record uuids of bullets that hit
				bulletsThatHitMe.append(bullet.uuid)
		
		# ===== Limit speed to player.MAXSPEED ===== #
		if vecMagnitude(self.deltaX)>player.MAXSPEED:
			vecScale(self.deltaX, player.MAXSPEED)

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

		self.id=canvas.create_image(player.RADIUS*2, player.RADIUS*2, image=photoimage)
	
	def update(self):
		pass
	
# ===== Bullets are shot by the square ===== #
class Bullet:
	RADIUS=5
	SPEED=10
	TTL=2000

	def __init__(self, pointer): # pointer refers to position of mouse pointer
		objects.append(self)
		bullets.append(self)
		
		# Direction vector along which bullet will travel
		direction=[pointer[0]-player.position[0], pointer[1]-player.position[1]] 
		self.deltaX=vecScale(direction,self.SPEED)

		self.id=canvas.create_oval(player.position[0]-self.RADIUS,player.position[1]+self.RADIUS,player.position[0]+self.RADIUS,player.position[1]-self.RADIUS, fill="red")
		root.after(self.TTL, self.vanish)
		
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


class OpponentBullet:
	def __init__(self):
		self.id=canvas.create_oval(0,0,10,10, fill="blue")

		#this will be updated by updateBullets()
		self.uuid=0


def gfxInit():
	global player
	global opponent
	print 'restarting'
	canvas.delete(ALL)

	while len(objects):
		del objects[0]
	while len(opponentBullets):
		del opponentBullets[0]
	while len(bullets):
		del bullets[0]
	
	player=Player()
	opponent=Opponent()


def onKey(event):
	#key press
	if event.type=="2":
		if event.keysym == "r":
			restartfn(False)
		if event.keysym == "b":
			print "DEBUG DATA:"
			print "Player coords: ", canvas.coords(player.id)
			print "Player move vector: ", player.deltaX, " speed=", vecMagnitude(player.deltaX)
		if event.keysym == "x":
			player.deltaX=[0,0]
		elif event.keysym in ["w","a","s","d"]:
			pressedKeys[event.keysym]=True
		elif event.keysym in ["<Escape>", "q"]:
			exit()
		return
	#key release
	elif event.type=="3":
		pressedKeys[event.keysym]=False
		return
	print 'ERROR:',event.type


def onClick(event):
	
	# Coordinates of mouse at click
	Bullet([event.x, event.y])
	
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
