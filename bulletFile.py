from Tkinter import *
from math import *

objects=[]
canvas=None
root=None
player=None

# ===== Bullets are shot by the square ===== #
class Bullet:
	def __init__(self, pointer): # pointer refers to position of mouse pointer
		objects.append(self)
		

		playerPos=[(player.position[2]+player.position[0])/2, (player.position[3]+player.position[1])/2] # Shoot from the center
		self.id=canvas.create_line(playerPos, pointer, fill="red", dash=(4,4))

		root.after(100, self.vanish)
		
	def vanish(self):
		canvas.delete(self.id)

		#this is called more than once for some reason
		objects.remove(self)

	def update(self):
		pass