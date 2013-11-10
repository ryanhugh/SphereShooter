from Tkinter import *
from random import *

root=None
upperFrame=None

scoreLabelVar=None
scoreLabel=None
lives=5

def setLives(thelives):
	global lives
	lives=thelives
	scoreLabelVar.set(int(lives))
	

def scoreboardInit():
	global scoreLabelVar
	global scoreLabel

	Label(upperFrame,text="Lives:").grid(row=0,column=1)

	scoreLabelVar=StringVar()
	scoreLabelVar.set(int(lives))

	scoreLabel=Label(upperFrame,textvariable=scoreLabelVar).grid(row=0,column=2)


if __name__ == '__main__':
	import mainfile
