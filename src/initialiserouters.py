import sys, socket


def init(input_ports):
    # Set up a UDP socket for each input ports (none needed for output ports)
    input_sockets = []
    for index in range(len(input_ports)):
        portnum = input_ports[index]
        daemon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        daemon.bind(('localhost', portnum))
        daemon.setblocking(False)
        input_sockets.append(daemon)

    # print("The socket info is:\n", [x.getsockname() for x in input_sockets])
    # print([type(x) for x in input_sockets])

    for index in range(len(input_sockets)):
        network, portnum = input_sockets[index].getsockname()
        print("Socket created on network {} with port number {}.".format(network, portnum))

    return input_sockets
