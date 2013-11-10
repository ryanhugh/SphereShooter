from Tkinter import *
from random import *

import helper
from helper import *

# ===== Initialized empty, Updated by mainfile ===== #
root=None
upperFrame=None



# ===== Important variables for this file ===== #
#your score
scoreLabelVar=None
scoreLabel=None

#opponent's score
otherScoreLabelVar=None
otherScoreLabel=None


def updateLivesLabel():
	scoreLabelVar.set(str(helper.player.lives))


def scoreboardInit():
	global scoreLabelVar
	global scoreLabel
	global otherScoreLabelVar
	global otherScoreLabel

	#"Lives:" label
	Label(upperFrame,text="Lives:").grid(row=0,column=1)

	#score label
	#keep the data of the score label in a StrinVar() so it can be updated
	scoreLabelVar=StringVar()
	scoreLabelVar.set(str(PLAYERLIVES))

	scoreLabel=Label(upperFrame,textvariable=scoreLabelVar).grid(row=0,column=2)


	#padding
	Label(upperFrame,text="                                            ").grid(row=0,column=3)


	#"Opponent's Lives:" label
	Label(upperFrame,text="Opponent's Lives:").grid(row=0,column=4)

	#Opponent's score label
	otherScoreLabelVar=StringVar()
	otherScoreLabelVar.set("20")

	scoreLabel=Label(upperFrame,textvariable=otherScoreLabelVar).grid(row=0,column=5)


if __name__ == '__main__':
	import mainfile
