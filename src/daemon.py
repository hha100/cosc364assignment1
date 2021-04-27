import sys, socket, routingtable, configparser, select, packet


def connect_socket(input_port):
    # Create TCP/IP socket and binds to the given port
    daemon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # daemon.setblocking(False)
    daemon.bind(('localhost', input_port))
    return daemon


def entry_to_string(rip_entry):
    destination, costs, next_hop, flag, came_from = rip_entry.get_info()
    string = "{0}_{1}_{2}_{3}_{4}".format(destination, costs, next_hop, flag, came_from)
    print("entry_to_string is: {}".format(string))
    return string


def string_to_entry(string):

    # Split the string into entry values and generate a new RIPEntry
    entry = routingtable.RIPEntry()
    values = string.split("_")
    entry.destination = values[0]
    entry.costs = values[1]
    entry.next_hop = values[2]
    entry.flag = values[3]
    # ToDo: Change the came_from here? or should this be done somewhere else? let's see....
    entry.came_from = values[4]
    print("Finished parsing string to entry. RIPEntry is:\n{}".format(entry))
    return entry


class Daemon:

    def __init__(self):
        self.rip_table = []
        self.input_ports = []
        self.output_ports = []
        self.open_sockets = []

    def init(self, input_ports):
        # Set up a UDP socket for each input ports (none needed for output ports)
        input_sockets = []
        for index in range(len(input_ports)):

            portnum = input_ports[index]
            daemon = connect_socket(portnum)
            # print("index: {}\ndaemon: {}".format(index, daemon))
            # daemon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # daemon.bind(('localhost', portnum))
            # daemon.setblocking(False)
            input_sockets.append(daemon)

        # print("The socket info is:\n", [x.getsockname() for x in input_sockets])
        # print([type(x) for x in input_sockets])

        for index in range(len(input_sockets)):
            network, portnum = input_sockets[index].getsockname()
            print("Socket created on network {} with port number {}.".format(network, portnum))

        return input_sockets

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
                        cost_to_connection = 1  # Assume the metric/cost to a connected router or network is 1
                        # Maybe an if to check if incoming is to the directly connected network? And pass it on? or would that logic be somewhere else like in main
                        total_incoming_cost = inc_costs + cost_to_connection
                        # ToDo: When sending out a table, add your own came_from to all entries (set your own router ID to it)
                        # ToDo: Make sure data is valid
                        # Here is the actual comparison code
                        if (total_incoming_cost < rip_costs) or ((inc_came_from == rip_came_from) and (
                                (total_incoming_cost != rip_costs) or (inc_flag != rip_flag) or (
                                inc_next_hop != rip_next_hop))):
                            incoming_table_entry.costs = total_incoming_cost
                            self.rip_table.update_entry(rip_table_entry, incoming_table_entry)

        print("Routing Table comparison complete.")
        return self.rip_table

        # print("{0} \n {1} \n {2} \n {3} \n {4}".format(destination, costs, next_hop, flag, came_from))  # For debugging

    def broadcast_table(self, input_sockets=[]):
        # print("Attempting to send my table to all neighbours...")
        # print("...But there's no sending logic yet")
        print("Sending my routing table to all neighbours...")

        ip = "localhost"
        dest_list = []

        # Get list of neighbours/direct connections
        # Create list of neighbours
        for output_port in self.output_ports:
            print("----OUTPORT PORT BEING ADDED TO DEST_LIST: {}".format(output_port[0]))
            dest = (ip, output_port[0])
            dest_list.append(dest)
        # ToDo: we want dest_list = list of ip addresses and their ports [(ip, port), (ip, port)]
        print("Made it past 1st for loop")
        print("dest_list is: {}".format(dest_list))

        # Create packet with table to send
        # Turn RIP table into data to send
        table_data = ''
        # table_data = packet.table_to_packet(self.rip_table)
        table_entries = self.rip_table.entries
        print("ENTRIES in self.rip_table.entries:\n")
        packets = []
        for entry in table_entries:
            print(entry)
            new_entry = entry_to_string(entry)
            packets.append(bytes(new_entry, "utf-8"))

        print("\nMade it past packet to bytes loop step\n")
        print("Packets is: {}".format(packets))
        sending_socket = self.open_sockets[0]
        print("pre destination")
        for destination in dest_list:
            print("NEW DESTINATION-----------\nDest: {}".format(destination))
            print("connecting to router\ndestination[1] is: {}".format(destination[1]))
            sending_socket.connect(destination)
            print("connected to router")
            for pack in packets:
                print("about to send packet")
                print("self.open_sockets are: {}\nsending_socket is: {}".format(self.open_sockets, sending_socket))
                # Connect to the router


                # And then send
                self.open_sockets[0].sendto(pack, destination)
                print("packet sent!!")
        print("\n---------Finished broadcasting table. -----------\n")

    # Infinite Loop

    def start_loop(self, config_filename):
        print("initializing... (start of loop function, before loop)")
        config_filename, router_id, self.input_ports, self.output_ports, timeouts = configparser.parse(config_filename)
        self.rip_table = routingtable.init_table(config_filename, self.output_ports)
        input_sockets = self.init(self.input_ports)
        self.open_sockets = input_sockets
        print("output ports!!!")
        for op in self.output_ports:
            print("op: {}".format(op))

        try:
            while True:
                # use select() to block until events occur
                print("while loop")
                # Check our neighbour routers and make sure we can still access them all
                # Send out the current table

                # If a table is received from another router....
                # rip_table = compare_tables(rip_table, incoming_table)
                # break

                # If self.open_sockets is not empty, run the select() function to listen to all sockets at the same time
                if self.open_sockets:
                    print("self.open_sockets is:\n{}".format(self.open_sockets))
                    # Uncomment the below code to run broadcast_table in while loop
                    self.broadcast_table()
                    # ToDo: remove the number 2 and have a variable in its place (it represents timeout of select function)
                    readable, writable, exceptional = select.select(self.open_sockets, [], self.open_sockets, 2)
                    print(
                        "Select statement done.\nreadable: {0}\nwritable: {1}\nexceptional: {2}".format(readable,
                                                                                                        writable,
                                                                                                        exceptional))
                    # for s in readable:

                    # connection, client_address = s.accept()

                    # response = into_packet(
                    # if response is not None:
                    #     s.sendto(byte_message, (client_ip_address, port_number))
                    # s.sendto(encoded_message, target_destination)

                    # for s in exceptional:
                    #    print("Select() exceptional error\nsocket: {}".format(socket))

                # Look into python's socket import receive and send functions
        except KeyboardInterrupt:
            print("User aborted program with Ctrl C")
            pass
        except:
            print("An error occurred (exception in daemon start_loop)")
            sys.exit()
