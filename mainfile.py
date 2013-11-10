import network
from network import *
import helper
from helper import *

from Tkinter import *
from random import *


root=Tk()


frame=Frame()
frame.grid(row=0,column=0)

canvas=Canvas(frame,width=500,height=500)
canvas.grid(row=0,column=0)

lowerFrame=Frame(width=root.winfo_screenwidth())
lowerFrame.grid(row=1,column=0)

objects=[]


helper.objects=objects
helper.canvas=canvas
helper.root=root

#these functions run with the update()
#copy the coordinates from network.newPlayerCoords to the Opponent data
def updateOpponent():
	canvas.coords(helper.opponent.id, *network.newPlayerCoords)

def updateBullets():

	while len(helper.bullets)>len(network.newBulletCorrds):
		del helper.bullets[-1]

	while len(helper.bullets)<len(network.newBulletCorrds):
		break
		# helper.otherbullets.append(2)
		#make a bullet! - FIXME

	for count,bulletCoords in enumerate(network.newBulletCorrds):
		if None in bulletCoords:
			print 'djfalsdjfslkd'
			print network.newBulletCorrds
			exit()
	

#send importiant stuff to network
network.lowerFrame=lowerFrame
network.root=root
network.updateOpponent=updateOpponent
network.updateBullets=updateBullets



def update():
	for obj in objects:
		obj.update()


	#send coords of everything
	network.addToSend([int(i) for i in helper.player.position])

	bulletCoords=[]

	#make array of coords from bullets
	for count,bullet in enumerate(helper.bullets):
		bulletCoords.append(canvas.coords(bullet.id))

	#make all coords ints
	for count,item in enumerate(bulletCoords):
		bulletCoords[count]=[int(i) for i in item]


	network.addToSend(bulletCoords)
	network.send()


	#if there is no opponent, don't update Opponent and Opponent bullets
	if network.destIp:
		updateBullets()
		updateOpponent()

	#schedual this funciton again
	root.after(10,update)


# ===== Keybinding ===== #
# w,a,s,d -> move
# r -> restart
# ESC,q -> quit
# b -> debug
root.bind("<Key>", onKey)
root.bind("<Button-1>", onClick)

Button(lowerFrame, text="Restart",command=gfxInit).grid(row=1,column=0)

#start update loop
root.after(10,update)

# ===== Init functions ===== #
gfxInit()
networkInit()

root.mainloop()


