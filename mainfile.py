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


def updateOpponent(coords):
	#move opponate to these coords

	# helper.opponate.coords=
	# print 'setting enemy to corrds:',coords

	canvas.coords(helper.opponent.id, *coords)
	# exit()
	
network.lowerFrame=lowerFrame
network.root=root
network.updateOpponent=updateOpponent



def update():
	for obj in objects:
		obj.update()

	root.after(10,update)


	network.addToSend(canvas.coords(helper.player.id))
	network.send()


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


