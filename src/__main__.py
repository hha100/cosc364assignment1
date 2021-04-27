"""__main__.py is run by default when naming the directory in the command line, meaning you don't need to specify
which file you want to run
e.g. 'py src conf/config1.txt' """

import daemon, sys


# def send_table(rip_table):

def compare_tables(rip_table, incoming_table):
    """
    Compares any two routing tables, and updates any relevant entries in table 1
    """

    # ToDo: I think i need to change all these self comparisons to "server" comparisons cause if this is run on the incoming table self. will always be the .. yanow
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
                            inc_came_from == rip_came_from) and ((total_incoming_cost != rip_costs) or (inc_flag != rip_flag) or (inc_next_hop != rip_next_hop))):
                        incoming_table_entry.costs = total_incoming_cost
                        rip_table.update_entry(rip_table_entry, incoming_table_entry)

    print("Routing Table comparison complete.")

    # print("{0} \n {1} \n {2} \n {3} \n {4}".format(destination, costs, next_hop, flag, came_from))  # For debugging


def main():
    """
    Main code to be run
    """
    if len(sys.argv) > 1:  # If there is a command line argument
        config_filename = str(sys.argv[1])
    else:
        print("\nConfig filename not detected. Please use a command line argument of the form 'router1_config.txt'.\n")
        sys.exit()  # Exit the program with an error message if there is no command line argument

    config_filename = str(sys.argv[1])

    print()

    # print() print("Routing table object, plus filename and entries are:\n{}\n{}\n{}".format(rip_table, rip_table.config_file, rip_table.entries))   # for debugging

    # print("\nInitial routing table entries are as follows:\n")
    #
    # i = 1
    # for entry in rip_table.get_table():
    #     print(i)
    #     print(entry)
    #     i += 1

    # Do the main loop of the routing daemon here after config file parsed, routers initialised, and initial routing table populated.
    daemon.start_loop(config_filename)

    # If a table is received from another router....
    #
    # compare_tables(rip_table, incoming_table)
    # break
    # except:
    #     print("Program ran into an error while routing.\n")
    #     sys.exit()


if __name__ == "__main__":
    main()
