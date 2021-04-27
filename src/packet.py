class Packet:

    def __init__(self, port, routes=[]):
        self.port = port
        self.routes = routes

    def to_packet(self, message):

        # Encodes message as a utf-8 byte string
        encoded_message = bytes(message, "utf-8")
        return encoded_message
