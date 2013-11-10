import re
from Tkinter import *
import socket
import SocketServer
import threading
import ast

root=None
lowerFrame=None
ipTextBox=None
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

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(*data):
	global dataToSend

	#if the regex fails, don't send anything
	if destIp==None:
		return

	sock.sendto(str(dataToSend), (destIp, PORT))

	dataToSend=[]


def addToSend(data):
	dataToSend.append(data)


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
    	global newPlayerCoords
    	global newBulletCoords
    	global recievedBulletsToStopSending

    	# get data
        clientAddr=self.client_address[0]
        data = ast.literal_eval(self.request[0])
        
        # incoming is list:
        # 1: list of player coords
        # 2: list of bullets
        	# each bullets coords


        newPlayerCoords=data[0]
        newBulletCoords=data[1]
        # for bulletcoord in newBulletCoords:
        # 	if  len(bulletcoord)==2:
        # 		print "uh oh!!"
        # 		newBulletCoords=[]
        # 		break
        recievedBulletsToStopSending=data[2]

        
                    

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

	# padding between box and ip
	Label(lowerFrame,text="                                            ").grid(row=1,column=1)
	

	#label and text box
	Label(lowerFrame,text="ip Address:").grid(row=1,column=2)

	ipTextBox = Entry(lowerFrame)
	ipTextBox.grid(row=1,column=3,padx=50)

	currentIp=waitForWifi()

	#for testing
	ipTextBox.insert(0,currentIp)
	enterButtonClicked(9)


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