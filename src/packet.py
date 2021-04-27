def table_to_packet(rip_table):
    encoded_table = ''
    # ToDo: Encode the RIP table into a format where it can be sent via a socket
    print("Encoding RIP table... no code here yet (packet.py) ")
    return encoded_table


class Packet:

    def __init__(self, port, routes=[]):
        self.port = port
        self.routes = routes

    def to_packet(self, message):

        # Encodes message as a utf-8 byte string
        encoded_message = bytes(message, "utf-8")
        return encoded_message
