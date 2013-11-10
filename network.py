import re
from Tkinter import *
import socket
import SocketServer
import threading
import ast

root=None
lowerFrame=None
ipTextBox=None
ipTextBoxVar=None
updateOpponent=None
updateBullets=None


#tkinter is not thread safe, and the recieving data is in a thread 
# so save this and update it in canvas on update
newPlayerCoords=[]
newBulletCoords=[]
recievedBulletsToStopSending=[]


#local server stuff
PORT =  4242

destIp=None

dataToSend=[]


doRestart=False
newOtherScore=""

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
	


def addToSend(data):
	dataToSend.append(data)


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
    	global newPlayerCoords
    	global newBulletCoords
    	global recievedBulletsToStopSending
    	global destIp
    	global doRestart
    	global newOtherScore

    	# get data
        clientAddr=self.client_address[0]
        if destIp!=clientAddr:
        	destIp=clientAddr
        	ipTextBoxVar.set(clientAddr)

        data = self.request[0]

        if data=="restart!":
        	doRestart=True
        	print 'told to restart!'
        	return

        data = ast.literal_eval(data)

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
def waitForWifi():
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

	#unfocus text box
	root.focus_set()

	#validate ip
	if not re.match(r'(\d+\.){3}\d+',ipTextBox.get()):
		print "invalid ip address"
		destIp=None
		return

	destIp=ipTextBox.get()
	print 'valid ip'


def networkInit():
	global ipTextBox
	global ipTextBoxVar

	# padding between box and ip
	Label(lowerFrame,text="                                            ").grid(row=1,column=1)
	

	#label and text box
	Label(lowerFrame,text="ip Address:").grid(row=1,column=2)


	currentIp=waitForWifi()


	ipTextBoxVar=StringVar()
	ipTextBoxVar.set(currentIp)

	ipTextBox = Entry(lowerFrame,textvariable=ipTextBoxVar)
	ipTextBox.grid(row=1,column=3,padx=50)

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
	import mainfile