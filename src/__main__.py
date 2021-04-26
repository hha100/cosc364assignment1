"""__main__.py is run by default when naming the directory in the command line, meaning you don't need to specify
which file you want to run
e.g. 'py src conf/config1.txt' """

import routingtable, configparser, initialiserouters, sys

def send_table(rip_table):



def compare(incoming_table):
    """
    Compares an incoming table with the current routing table, and updates any entries that should be updated
    """
    


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
    config_filename, router_id, input_ports, output_ports, timeouts = configparser.parse(config_filename)
    input_sockets = initialiserouters.init(input_ports)
    rip_table = routingtable.init_table(config_filename, output_ports)

    print()

    # print() print("Routing table object, plus filename and entries are:\n{}\n{}\n{}".format(rip_table, rip_table.config_file, rip_table.entries))   # for debugging

    print("\nInitial routing table entries are as follows:\n")

    i = 1
    for entry in rip_table.get_table():
        print(i)
        print(entry)
        i += 1

    # Do the main loop of the routing daemon here after config file parsed, routers initialised, and initial routing table populated.
    try:
        while True:
            # use select() to block until events occur
            print("while loop")
            #Send out the current table
            send_table(rip_table)
            # If a table is received from another router....
            # compare(incoming_table)
            break
    except:
        print("Program ran into an error while routing.\n")
        sys.exit()


if __name__ == "__main__":
    main()
