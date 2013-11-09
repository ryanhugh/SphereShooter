import re
from Tkinter import *
import socket
import SocketServer
import threading

root=None
lowerFrame=None
ipTextBox=None


#local server stuff
PORT =  9999

destIp=None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

dataToSend=[]

def send(*data):
	global dataToSend

	if destIp==None:
		return
	print 'sending',dataToSend,' to',destIp
	

	sock.sendto(str(dataToSend), (destIp, PORT))

	dataToSend=[]


def addToSend(*data):
	dataToSend.append(str(data))



	

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        clientAddr=self.client_address[0]
        data = self.request[0]
        print data
        
        
                    

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

	# print root.coords(ipTextBox)

def boxClicked():
	print 'hi'



def networkInit():
	global ipTextBox

	# padding between box and ip
	Label(lowerFrame,text="                                            ").grid(row=1,column=1)
	


	Label(lowerFrame,text="ip Address:").grid(row=1,column=2)

	ipTextBox = Entry(lowerFrame)
	ipTextBox.grid(row=1,column=3,padx=50)



	root.bind("<Return>", enterButtonClicked)



	#make a UDP server
	server = ThreadedUDPServer((waitForWifi(), PORT), ThreadedUDPRequestHandler)

	#and put it in a thread
	server_thread = threading.Thread(target=server.serve_forever)

	server_thread.daemon = True
	server_thread.start()






if __name__ == '__main__':
	import mainfile