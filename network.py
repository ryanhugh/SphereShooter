import re
from Tkinter import *
import socket
import SocketServer
import threading
import ast
import time
import pyclip

# ===== Constants ===== #
PORT =  4242
CONNECTIONTIMEOUT=2000

# ===== Initialized empty, Updated by mainfile ===== #
root=None
lowerFrame=None
updateOpponent=None
updateBullets=None


# ===== Important variables for this file ===== #
ipTextBox=None
ipTextBoxVar=None

OppStatusBox=None
OppStatusBoxVar=None

TimeSinceLastPacket=0
isConnected=False



#tkinter is not thread safe, - all these act as buffers to communicate between threads

#received player and bullet coords
newPlayerCoords=[]
newBulletCoords=[]

#bullet that hit opponent
recievedBulletsToStopSending=[]

#opponent sent restart message
doRestart=False
iWon=False

#opponent's score
newOtherScore=""

#network stuff
destIp=None

dataToSend=[]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(*data):
	global dataToSend

	#if the regex fails, don't send anything
	if destIp==None:
		return

	sock.sendto(str(dataToSend), (destIp, PORT))

	dataToSend=[]



def sendRestartMsg():
	sock.sendto("restart!", (destIp, PORT))
	sock.sendto("restart!", (destIp, PORT))
	sock.sendto("restart!", (destIp, PORT))
	

def sendLoseMsg():
	sock.sendto("ILose!", (destIp, PORT))
	sock.sendto("ILose!", (destIp, PORT))
	sock.sendto("ILose!", (destIp, PORT))
	


def addToSend(data):
	dataToSend.append(data)


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		global newPlayerCoords
		global newBulletCoords
		global newOtherScore
		global recievedBulletsToStopSending
		global destIp
		global doRestart
		global TimeSinceLastPacket
		global isConnected
		global iWon


		TimeSinceLastPacket=time.time()
		if not isConnected:
			print 'Connected!'
			isConnected=True
			OppStatusBoxVar.set("Connected")
			OppStatusBox.config(fg='green')


		# get data
		clientAddr=self.client_address[0]
		if destIp!=clientAddr:
			destIp=clientAddr
			ipTextBoxVar.set(clientAddr)

			
		if destIp==currentIp:
			OppStatusBoxVar.set("No Opponent!")
			OppStatusBox.config(fg='red')
		else:
			OppStatusBoxVar.set("Connected")
			OppStatusBox.config(fg='green')

		data = self.request[0]

		if data=="restart!":
			doRestart=True
			print 'told to restart!'
			return

		if data=="ILose!":
			iWon=True
			print 'told that i have won!'
			return


		try:
			data = ast.literal_eval(data)
		except Exception as e:
			print 'bad packet!',e
			print data
			return

		# incoming is list:
		# 1: list of player coords
		# 2: list of bullets
			# each bullets coords
		# 3 uuids of each bullet that should be deleted
		# other person's score

		newPlayerCoords=data[0]
		newBulletCoords=data[1]


		recievedBulletsToStopSending=data[2]
		
		newOtherScore=str(data[3])

		
					

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
	pass


#waits for wifi to start up and obtain a ip address
def getIpAddress():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while 42:
		sockport='192.168.0.100'
		try:

			#try to connect to some other ip
			s.connect((sockport, 9999))

			#if wifi is up, this will be current ip address
			currentIp=s.getsockname()[0]

			#then close the connection
			s.close()
			print 'current ip:',currentIp
			
			return currentIp
		except:
			print 'ERROR:could not open socket to ',sockport,'!'

		#wait before trying again
		time.sleep(1)



def enterButtonClicked(event):
	global destIp
	global isConnected

	#unfocus text box
	root.focus_set()

	#validate ip
	if not re.match(r'(\d+\.){3}\d+$',ipTextBox.get()):
		print "invalid ip address"
		destIp=None
		isConnected=False
		OppStatusBoxVar.set("Invalid IP Address")
		OppStatusBox.config(fg='red')
		return

	destIp=ipTextBox.get()
	print 'valid ip'


def networkInit():
	global ipTextBox
	global ipTextBoxVar
	global OppStatusBox
	global OppStatusBoxVar
	global currentIp

	# padding between box and ip
	Label(lowerFrame,text="                                            ").grid(row=1,column=1)
	

	#label and text box
	Label(lowerFrame,text="ip Address:").grid(row=1,column=2)


	currentIp=getIpAddress()

	#ip Entry 
	ipTextBoxVar=StringVar()
	ipTextBoxVar.set(currentIp)

	ipTextBox = Entry(lowerFrame,textvariable=ipTextBoxVar)
	ipTextBox.grid(row=1,column=3,padx=5)

	#opponent status
	OppStatusBoxVar=StringVar()
	OppStatusBoxVar.set("Not connected")

	OppStatusBox = Label(lowerFrame,textvariable=OppStatusBoxVar)
	OppStatusBox.grid(row=1,column=4)
	OppStatusBox.config(fg='red')



	# padding
	Label(lowerFrame,text="            ",pady=5).grid(row=1,column=5)


	# padding
	Label(lowerFrame,text="Current IP:  "+currentIp).grid(row=1,column=6,padx=5)


	Button(lowerFrame, text="Copy",command=lambda: pyclip.copy(currentIp)).grid(row=1,column=7)



	#for testing
	enterButtonClicked(42)


	#unfocus text box when enter is clicked
	root.bind("<Return>", enterButtonClicked)

	#make a UDP server
	server = ThreadedUDPServer((currentIp, PORT), ThreadedUDPRequestHandler)

	#and put it in a thread
	server_thread = threading.Thread(target=server.serve_forever)

	server_thread.daemon = True
	server_thread.start()



if __name__ == '__main__':
	import main
