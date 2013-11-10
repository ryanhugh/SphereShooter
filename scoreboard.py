from Tkinter import *
from random import *

import helper
from helper import *

root=None
upperFrame=None

scoreLabelVar=None
scoreLabel=None

otherScore=""

otherScoreLabelVar=None
otherScoreLabel=None


def setLives(thelives):
	helper.player.lives=thelives
	scoreLabelVar.set(int(helper.player.lives))


def scoreboardInit():
	global scoreLabelVar
	global scoreLabel
	global otherScoreLabelVar
	global otherScoreLabel

	Label(upperFrame,text="Lives:").grid(row=0,column=1)

	scoreLabelVar=StringVar()
	scoreLabelVar.set(int(helper.player.lives))

	scoreLabel=Label(upperFrame,textvariable=scoreLabelVar).grid(row=0,column=2)


	Label(upperFrame,text="                                            ").grid(row=0,column=3)


	Label(upperFrame,text="Opponent's Lives:").grid(row=0,column=4)

	otherScoreLabelVar=StringVar()
	otherScoreLabelVar.set("20")

	scoreLabel=Label(upperFrame,textvariable=scoreLabelVar).grid(row=0,column=5)


if __name__ == '__main__':
	import mainfile
