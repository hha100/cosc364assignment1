import sys, socket, routingtable, configparser, select, packet


class Daemon:

    def __init__(self):
        self.rip_table = []
        self.input_ports = []
        self.output_ports = []

    def init(self, input_ports):
        # Set up a UDP socket for each input ports (none needed for output ports)
        input_sockets = []
        for index in range(len(input_ports)):
            portnum = input_ports[index]
            daemon = self.connect_socket(portnum)
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

    def connect_socket(self, input_port):
        # Create TCP/IP socket and binds to the given port
        daemon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        daemon.setblocking(False)
        daemon.bind(('localhost', input_port))
        return daemon

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
            dest = (ip, output_port)
            dest_list.append(dest)
        # ToDo: we want dest_list = list of ip addresses and their ports [(ip, port), (ip, port)]
        print("Made it past 1st for loop")

        # Create packet with table to send
        # Turn RIP table into data to send
        table_data = ''
        print("self.rip_table is: {}".format(self.rip_table))
        packet = bytes(table_data, "utf-8")
        print("Made it past packet bytes step")

        for destination in dest_list:
            input_sockets[0].sendto(packet, destination)

    # Infinite Loop

    def start_loop(self, config_filename):
        print("initializing... (start of loop function, before loop)")
        config_filename, router_id, self.input_ports, self.output_ports, timeouts = configparser.parse(config_filename)
        self.rip_table = routingtable.init_table(config_filename, self.output_ports)
        input_sockets = self.init(self.input_ports)
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

                # If input_sockets is not empty, run the select() function to listen to all sockets at the same time
                if input_sockets:
                    print("input_sockets is:\n{}".format(input_sockets))
                    # Uncomment the below code to run broadcast_table in while loop
                    # self.broadcast_table(input_sockets, self.output_ports)
                    # ToDo: remove the number 2 and have a variable in its place (it represents timeout of select function)
                    readable, writable, exceptional = select.select(input_sockets, [], input_sockets, 2)
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
