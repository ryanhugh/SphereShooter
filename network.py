from Tkinter import *
import socket
import SocketServer
import threading

root=None
frame=None
ipTextBox=None




sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def send():
	print 'sending',ipTextBox.get()
	pass



	

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        clientAddr=self.client_address[0]
        data = self.request[0]
        
        
                    

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
	root.focus_set()
	print root.coords(ipTextBox)

def boxClicked():
	print 'hi'



def networkInit():
	global ipTextBox
	ipTextBox = Entry(frame)#,command=boxClicked)
	ipTextBox.pack()


	root.bind("<Return>", enterButtonClicked)


	# print ipTextBox

	#local server stuff
	PORT =  9999

	#make a UDP server
	server = ThreadedUDPServer((waitForWifi(), PORT), ThreadedUDPRequestHandler)

	#and put it in a thread
	server_thread = threading.Thread(target=server.serve_forever)

	server_thread.daemon = True
	server_thread.start()






if __name__ == '__main__':
	import mainfile