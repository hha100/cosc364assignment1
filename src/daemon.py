import sys, socket, routingtable, configparser, select, time

def connect_socket(input_port):
    """Creates a UDP socket and bind it to the given port"""
    
    # Create a socket configured to send/recieve UDP datagrams with blocking enabled and bind it to the given input port
    daemon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    daemon.setblocking(True)
    daemon.bind(('localhost', input_port))
    
    # Return the socket
    return daemon


def string_to_entry(string):
    """ Splits the string into routing table entry values and generate a new RIPEntry"""
    
    # Create a new RIPEntry instance
    entry = routingtable.RIPEntry()
    
    # Split the value string (consisting of underscore separated integers) into a list of values
    values = string.split("_")
    
    # Add these values to the RIPEntry instance
    entry.destination = values[0]
    entry.costs = values[1]
    entry.next_hop = values[2]
    entry.flag = values[3]
    entry.came_from = values[4]
    
    # Print a confirmation message and return the entry
    print("Finished parsing string to entry. RIPEntry is:\n{}".format(entry))
    return entry


class Daemon:
    """ A class to create the routing daemon with its own RIP routing table, sockets and config file parameters which can communicate with other routers."""
    
    def __init__(self):
        """ Initialise all the routing daemon values"""
        
        self.rip_table = []
        self.input_ports = []
        self.output_ports = []
        self.open_sockets = []
        self.router_id = None
        self.timeouts = None

    def init(self, input_ports):
        """ Set up a UDP socket for each input port (none needed for output ports)"""
        
        input_sockets = []
        
        # Iterate through the input ports
        for index in range(len(input_ports)):
            
            # Take the port number and create a UDP socket bound to it
            portnum = input_ports[index]
            daemon = connect_socket(portnum)
            
            # Append the input socket to a list of sockets
            input_sockets.append(daemon)
        
        # Iterate throguh the input socket list and print a message confirming their successful creation
        for index in range(len(input_sockets)):
            network, portnum = input_sockets[index].getsockname()
            print("Socket created on network {} with port number {}.".format(network, portnum))
        
        # Return the input socket list
        return input_sockets

    def entry_to_string(self, rip_entry):
        """ Turns a RIPEntry into a string that can be encoded and sent as a UDP datagram"""
        
        destination, costs, next_hop, flag, came_from = rip_entry.get_info()
        came_from = self.router_id
        string = "{0}_{1}_{2}_{3}_{4}".format(destination, costs, next_hop, flag, came_from)
        return string

    def compare_tables(self, incoming_table):
        """ Compares a given routing table with the Daemons routing table, and updates any relevant entries"""
        
        # Iterate through the entries in the received routing table
        for incoming_table_entry in incoming_table.get_table():
            
            # Retrieve the values from the RIPEntry
            inc_destination, inc_costs, inc_next_hop, inc_flag, inc_came_from = incoming_table_entry.get_info()
            
            # If the destination is not known to this router, add the entry to the Daemons routing table
            if inc_destination not in self.rip_table.get_table():
                
                # Add the entry to the 
                self.rip_table.add_to_table(incoming_table_entry)
            
            # If the destination is already known to this router
            else:
                
                # Iterate through the entries in this router
                for rip_table_entry in self.rip_table.get_table():
                    
                    # Get the values of the routing table entry
                    rip_destination, rip_costs, rip_next_hop, rip_flag, rip_came_from = rip_table_entry.get_info()
                    
                    # If the incoming routing table entry has the same destination as the local entry
                    if inc_destination == rip_destination():
                        cost_to_connection = 1
                        total_incoming_cost = inc_costs + cost_to_connection
                        
                        # If the path to a destination router has a lower cost than the local path
                        if (total_incoming_cost < rip_costs) or ((inc_came_from == rip_came_from) and ((total_incoming_cost != rip_costs) or (inc_flag != rip_flag) or (inc_next_hop != rip_next_hop))):
                            
                            # Update the local entry with the updated values
                            incoming_table_entry.costs = total_incoming_cost
                            self.rip_table.update_entry(rip_table_entry, incoming_table_entry)

        # Print a confimation message for the successful comparison
        print("Routing Table comparison complete.")

    def broadcast_table(self, input_sockets=[]):
        """ Sends the local routing table entries to all neighbouring routers"""
        
        # Initialise variables for the localhost IP address used by all routers and a list for destination routers
        ip = 'localhost'
        dest_list = []

        # Iterate through the output ports
        for output_port in self.output_ports:
            
            # Get the port number of each neighbouring router socket connection and add a tuple (IP, port number) to the destination router list
            dest = (ip, output_port[0])
            dest_list.append(dest)
        
        packets = []
        
        # Get the local routing table entries and select an arbitrary input socket to use to send messages to all output ports
        table_entries = self.rip_table.entries
        sending_socket = self.open_sockets[0]
        
        # Iterate through the entries in the local routing table
        for entry in table_entries:
            
            # Turn each entry into a string containing underscore separated values then encode the string and append it to the list of packets to be sent
            new_entry = self.entry_to_string(entry)
            new_encoded_entry = new_entry.encode()
            packets.append(new_encoded_entry)
        
        # Iterate through the (IP, port number) tuples in the destination router list
        for destination in dest_list:
            
            # Iterate through the packets to be sent
            for pack in packets:
                
                # Send the packets using the arbitrary input socket
                sending_socket.sendto(pack, destination)

    def start_loop(self, config_filename):
        """ Infinite loop where routing is carried out"""
        
        # Use the config file to get the router parameters
        config_filename, self.router_id, self.input_ports, self.output_ports, self.timeouts = configparser.parse(config_filename)
        
        # Initialise a routing table for this router
        self.rip_table = routingtable.init_table(config_filename, self.output_ports)
        
        # Create a list of input sockets
        input_sockets = self.init(self.input_ports)
        self.open_sockets = input_sockets
        
        # Try to enter an infinite loop
        try:
            
            # Loops infinitely
            while True:
                
                # Prints the local routing table one per while loop with ~ symbols used for text output formatting
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                for entry in self.rip_table.entries:
                    print(entry)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                
                # If self.open_sockets is not empty
                if self.open_sockets:
                    
                    # Send the local routing table to neighbouring routers
                    self.broadcast_table()
                    
                    # Use select() to check for changes to the input sockets
                    readable, writable, exceptional = select.select(self.open_sockets, [], self.open_sockets, 180)
                    
                    data, addr = False, ""
                    
                    # For each socket with a readable message
                    for s in readable:
                        
                        # If the message is not empty
                        if s:
                            
                            # Try to receive the data from the message and its source address
                            try:
                                data, addr = s.recvfrom(128)
                                
                            # If this fails, ignore the error and continue
                            except:
                                pass
                    
                    # If the data read from the message is not empty
                    if data:
                        
                        # Decode the data and split it into a list of values
                        data = data.decode('utf-8').split('_')
                        
                        # Print the values received from the data
                        print("Received Routing Entry From Router {}:\nData: {}\nAddr: {}".format(data[-1], data, addr))
                    
                    # Print a message to show that the code is waiting then sleep for 5 seconds
                    print('...')
                    time.sleep(5)
        
        # If the user presses Ctrl + C to exit the program from the infinite loop
        except KeyboardInterrupt:
            print("User aborted program with Ctrl C")
        
        # If an unknown error occurs in the infinite loop
        except:
            print("An error occurred (exception in daemon start_loop)")
