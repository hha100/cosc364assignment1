import sys, socket, routingtable, configparser, select, time

def connect_socket(input_port):
    # Create TCP/IP socket and binds to the given port
    daemon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    daemon.setblocking(True)
    daemon.bind(('localhost', input_port))
    return daemon


def string_to_entry(string):
    # Split the string into entry values and generate a new RIPEntry
    entry = routingtable.RIPEntry()
    values = string.split("_")
    entry.destination = values[0]
    entry.costs = values[1]
    entry.next_hop = values[2]
    entry.flag = values[3]
    entry.came_from = values[4]
    print("Finished parsing string to entry. RIPEntry is:\n{}".format(entry))
    return entry


class Daemon:

    def __init__(self):
        self.rip_table = []
        self.input_ports = []
        self.output_ports = []
        self.open_sockets = []
        self.router_id = None
        self.timeouts = None

    def init(self, input_ports):
        # Set up a UDP socket for each input ports (none needed for output ports)
        input_sockets = []
        for index in range(len(input_ports)):
            portnum = input_ports[index]
            daemon = connect_socket(portnum)
            input_sockets.append(daemon)

        for index in range(len(input_sockets)):
            network, portnum = input_sockets[index].getsockname()
            print("Socket created on network {} with port number {}.".format(network, portnum))

        return input_sockets

    def entry_to_string(self, rip_entry):
        destination, costs, next_hop, flag, came_from = rip_entry.get_info()
        came_from = self.router_id
        string = "{0}_{1}_{2}_{3}_{4}".format(destination, costs, next_hop, flag, came_from)
        return string

    def compare_tables(self, incoming_table):
        """
        Compares any two routing tables, and updates any relevant entries in table 1
        Returns the updated RIP Table
        """

        for incoming_table_entry in incoming_table.get_table():
            inc_destination, inc_costs, inc_next_hop, inc_flag, inc_came_from = incoming_table_entry.get_info()
            if inc_destination not in self.rip_table.get_table():
                self.rip_table.add_to_table(incoming_table_entry)
                print("Added new destination to table. Check back here cause i gotta rethink this code")
            else:
                for rip_table_entry in self.rip_table.get_table():
                    rip_destination, rip_costs, rip_next_hop, rip_flag, rip_came_from = rip_table_entry.get_info()
                    if inc_destination == rip_destination():
                        cost_to_connection = 1
                        total_incoming_cost = inc_costs + cost_to_connection
                        if (total_incoming_cost < rip_costs) or ((inc_came_from == rip_came_from) and (
                                (total_incoming_cost != rip_costs) or (inc_flag != rip_flag) or (
                                inc_next_hop != rip_next_hop))):
                            incoming_table_entry.costs = total_incoming_cost
                            self.rip_table.update_entry(rip_table_entry, incoming_table_entry)

        print("Routing Table comparison complete.")
        return self.rip_table

    def broadcast_table(self, input_sockets=[]):

        ip = 'localhost'
        dest_list = []

        # Get list of neighbours/direct connections
        # Create list of neighbours
        for output_port in self.output_ports:
            dest = (ip, output_port[0])
            dest_list.append(dest)
        table_entries = self.rip_table.entries
        packets = []
        sending_socket = self.open_sockets[0]
        for entry in table_entries:
            new_entry = self.entry_to_string(entry)
            new_encoded_entry = new_entry.encode()
            packets.append(new_encoded_entry)
            
        for destination in dest_list:
            for pack in packets:
                sending_socket.sendto(pack, destination)

    # Infinite Loop
    def start_loop(self, config_filename):
        config_filename, self.router_id, self.input_ports, self.output_ports, self.timeouts = configparser.parse(config_filename)
        
        self.rip_table = routingtable.init_table(config_filename, self.output_ports)
        input_sockets = self.init(self.input_ports)
        self.open_sockets = input_sockets

        try:
            while True:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                for entry in self.rip_table.entries:
                    print(entry)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                
                # If self.open_sockets is not empty, run the select() function to listen to all sockets at the same time
                if self.open_sockets:
                    self.broadcast_table()
                    readable, writable, exceptional = select.select(self.open_sockets, [], self.open_sockets, 180)
                    rec_socket = self.open_sockets[0]
                    rec_port = rec_socket.getsockname()[1]
                    data, addr = False, ""
                    for s in readable:
                        if s:
                            try:
                                data, addr = s.recvfrom(128)
                            except:
                                pass
                    
                    if data:
                        data = data.decode('utf-8').split('_')
                        print("Received Routing Entry From Router {}:\nData: {}\nAddr: {}".format(data[-1], data, addr))
                    
                    print('...')
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            print("User aborted program with Ctrl C")
            pass
        except:
            print("An error occurred (exception in daemon start_loop)")
