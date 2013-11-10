import network
from network import *

import helper
from helper import *

import scoreboard
from scoreboard import *

from Tkinter import *
from random import *


root=Tk()




frame=Frame()
frame.grid(row=1,column=0)

canvas=Canvas(frame,width=500,height=500)
canvas.grid(row=1,column=0)

upperFrame=Frame(width=root.winfo_screenwidth())
upperFrame.grid(row=0,column=0)

lowerFrame=Frame(width=root.winfo_screenwidth())
lowerFrame.grid(row=2,column=0)

objects=[]


#these functions run with the update()
#copy the coordinates from network.newPlayerCoords to the Opponent data
def updateOpponent():
	canvas.coords(helper.opponent.id, *network.newPlayerCoords)

def updateBullets():

	while len(helper.opponentBullets)>len(network.newBulletCoords):
		canvas.delete(helper.opponentBullets[-1])
		del helper.opponentBullets[-1]

	while len(helper.opponentBullets)<len(network.newBulletCoords):
		helper.opponentBullets.append(canvas.create_oval(0,0,10,10, fill="blue"))

	for count,bulletCoords in enumerate(network.newBulletCoords):

		canvas.coords(helper.opponentBullets[count],(bulletCoords[0],bulletCoords[1],10+bulletCoords[0],10+bulletCoords[1]))

	

#send importiant stuff to network
network.lowerFrame=lowerFrame
network.root=root
network.updateOpponent=updateOpponent
network.updateBullets=updateBullets


helper.objects=objects
helper.canvas=canvas
helper.root=root

scoreboard.upperFrame=upperFrame
scoreboard.root=root



def update():
	for obj in objects:
		obj.update()


	#send coords of everything
	network.addToSend([int(i) for i in canvas.coords(helper.player.id)])

	bulletCoords=[]

	# print len(helper.bullets)

	#make array of coords from bullets
	for count,bullet in enumerate(helper.bullets):
		bulletCoords.append(canvas.coords(bullet.id))

	#make all coords ints
	for count,item in enumerate(bulletCoords):
		bulletCoords[count]=[int(i) for i in item][0:2]

	# print bulletCoords

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
scoreboardInit()

root.mainloop()


