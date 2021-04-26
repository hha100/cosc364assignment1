import sys, socket, select


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


def compare_tables(rip_table, incoming_table):
    """
    Compares any two routing tables, and updates any relevant entries in table 1
    """
    for incoming_table_entry in incoming_table.get_table():
        inc_destination, inc_costs, inc_next_hop, inc_flag, inc_came_from = incoming_table_entry.get_info()
        if inc_destination not in rip_table.get_table():
            rip_table.add_to_table(incoming_table_entry)
            print("Added new destination to table. Check back here cause i gotta rethink this code")
        else:
            for rip_table_entry in rip_table.get_table():
                rip_destination, rip_costs, rip_next_hop, rip_flag, rip_came_from = rip_table_entry.get_info()
                if inc_destination == rip_destination():
                    cost_to_connection = 1  # Assume the metric/cost to a connected router or network is 1
                    # Maybe an if to check if incoming is to the directly connected network? And pass it on? or would that logic be somewhere else like in main
                    total_incoming_cost = inc_costs + cost_to_connection
                    # ToDo: When sending out a table, add your own came_from to all entries (set your own router ID to it)
                    # ToDo: Make sure data is valid
                    # Here is the actual comparison code
                    if (total_incoming_cost < rip_costs) or ((
                                                                     inc_came_from == rip_came_from) and (
                                                                     (total_incoming_cost != rip_costs) or (
                                                                     inc_flag != rip_flag) or (
                                                                             inc_next_hop != rip_next_hop))):
                        incoming_table_entry.costs = total_incoming_cost
                        rip_table.update_entry(rip_table_entry, incoming_table_entry)

    print("Routing Table comparison complete.")

    # print("{0} \n {1} \n {2} \n {3} \n {4}".format(destination, costs, next_hop, flag, came_from))  # For debugging


# Infinite Loop

def start_loop(input_ports):
    try:
        while True:
            # use select() to block until events occur
            print("while loop")
            # Send out the current table
            # send_table(rip_table)
            # If a table is received from another router....
            # compare_tables(rip_table, incoming_table)
            # break
            print("initializing...")
            input_sockets = init(input_ports)
            if input_sockets:
                print("input_sockets is:\n{}".format(input_sockets))
            readable, writable, exceptional = select.select([], [], input_ports)
            print("Select statement done.\nreadable: {0}\nwritable: {1}\nexceptional: {2}".format(readable, writable, exceptional))

    except:
        print("Program ran into an error while routing.\n")
        sys.exit()