import sys, socket, select

def init():
    try:
        #Set up a UDP socket for each input ports (none needed for output ports)
        input_sockets = []
        for index in range(len(input_ports)):
            portnum = input_ports[index]
            daemon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            daemon.bind(('localhost', portnum))
            daemon.listen(5)
        
        
        while True:
            #use select() to block until events occur
            pass
    except:
        print("Program ran into an error while initialising routing daemon.\n")
        sys.exit()