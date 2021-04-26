import sys, socket, select


def parse(conf_file):
    config = {}
    print()  # To aid with readability of the text output in terminal

    if len(sys.argv) > 1:  # If there is a command line argument
        """config_filename = str(sys.argv[1])  # Save the name of the config file for this router to a variable"""
        config_filename = conf_file
    else:
        print("Config filename not detected. Please use a command line argument of the form 'router1_config.txt'.\n")
        sys.exit()  # Exit the program with an error message if there is no command line argument

    try:
        file = open(config_filename, 'r')  # Try to open the file
        config_lines = file.readlines()  # Save the lines from the config file in a list
        file.close()  # Close the file
    except:
        print("File could not be found or is not a readable .txt file.\n")
        sys.exit()  # If the file can't be found and/or read, exit the program with an error message

    try:
        for index in range(len(config_lines)):
            config_lines[index] = [x.strip("\n") for x in config_lines[index].split(
                " ")]  # Split each line into strings and strip any newline characters
    except:
        print("Incorrect line format on line {} of config file.\n".format(index))
        sys.exit()  # Exit the program with an error message if there is a line in the config file that cannot be split into strings

    router_id = None
    input_ports = []  # Create an empty list to hold the input ports of this router
    output_ports = []  # Create an empty list to hold the output ports of this router
    timeout = 180  # Set the default timer interval to _____ ~~~~~(find a good default value later)~~~~~

    try:
        for line in config_lines:

            first_str = line[0]

            # If the line being read is assigning the router ID
            if first_str == "router-id":

                if router_id == None:
                    if line[1].isnumeric() == False:
                        print("Router ID must be an integer.\n")
                        sys.exit()
                    if int(line[1]) not in range(1, 64001):
                        print("Router ID must be between 1 and 64000.")
                        sys.exit()
                    else:
                        router_id = line[1]
                        print("Router ID assigned to {}\n".format(router_id))
                        config["router_id"] = router_id
                else:
                    print("Router ID must only be assigned once.\n")
                    sys.exit()

            # If the line being read is assigning the input ports
            elif first_str == "input-ports":
                for index in range(1, len(line)):
                    if line[index].isnumeric() == False:
                        print("ERROR: Input ports must be positive integers.\n")
                        sys.exit()
                    elif int(line[index]) in input_ports:
                        print("ERROR: Duplicate input port number detected.\n")
                        sys.exit()
                    elif int(line[index]) in [x[0] for x in output_ports]:
                        print("ERROR: An input port is already assigned as an output port.\n")
                        sys.exit()
                    elif int(line[index]) not in range(1024, 64001):
                        print("ERROR: All input ports in the config file must be between 1024 and 64000\n")
                        sys.exit()
                    else:
                        input_ports.append(int(line[index]))
                print("Input ports assigned to {}\n".format([x for x in input_ports]))
                config["input_ports"] = input_ports

            # If the line being read is assigning the output ports
            elif first_str == "output-ports":
                for index in range(1, len(line)):
                    # output_port = [int(x.strip("\n")) for x in line[index].split("-")]
                    output = line[index].split("-")
                    if len(output) != 3:
                        print(
                            "ERROR: The length of an output port definition is of incorrent length. Make sure output ports are of the form PORT-METRIC-ROUTER ID.\n")
                        sys.exit()
                    elif output[0].isnumeric() == False or output[1].isnumeric() == False or output[
                        2].isnumeric() == False:
                        print("ERROR: Output ports, metrics and router IDs must be positive integers.\n")
                        sys.exit()
                    elif int(output[0]) in input_ports:
                        print("ERROR: An output port is already assigned as an input port.\n")
                        sys.exit()
                    elif int(output[0]) in [x[0] for x in output_ports]:
                        print("ERROR: Duplicate output port number detected.\n")
                        sys.exit()
                    elif int(output[0]) not in range(1024, 64001):
                        print("ERROR: All output ports in the config file must be between 1024 and 64000\n")
                        sys.exit()
                    elif int(output[2]) == router_id:
                        print("ERROR: The router ID of one of the output ports matches the router ID of this router.\n")
                        sys.exit()
                    elif int(output[2]) not in range(1, 64001):
                        print("ERROR: The router ID of one of the output ports is not between 1 and 64000.\n")
                        sys.exit()
                    else:
                        output_ports.append([int(x) for x in output])
                print("Output ports assigned to {}".format([x[0] for x in output_ports]))
                config["output_ports"] = [x[0] for x in output_ports]
                print("Output metrics assigned to {}".format([x[1] for x in output_ports]))
                config["output_metrics"] = [x[1] for x in output_ports]
                print("Output router IDs assigned to {}\n".format([x[2] for x in output_ports]))
                config["output_router_ids"] = [x[2] for x in output_ports]


            # If the line being read is assigning the timeout interval
            elif first_str == "timeout":
                if line[1].isnumeric() == False:
                    print("ERROR: Timeout value is not an integer.\n")
                    sys.exit()
                elif int(line[1]) not in range(10, 181):
                    print("ERROR: Timeout interval must be an integer between 10 and 180 seconds.\n")
                    sys.exit()
                else:
                    timeout = int(line[1])
                    periodic_timer = int(timeout / 6)
                print("Timeout and periodic timer intervals are assigned to {} seconds and {} seconds\n".format(timeout,
                                                                                                                periodic_timer))
                config["timeout"] = timeout
                config["periodic_timer"] = periodic_timer

        error_msg = ""
        if router_id == None:
            error_msg += "ERROR: Router ID was not assigned in config file.\n"
        if input_ports == list():
            error_msg += "ERROR: Input ports not assigned in config file.\n"
        if output_ports == list():
            error_msg += "ERROR: Output ports not assigned in config file.\n"

        if error_msg != "":
            print(error_msg)
            sys.exit()


    except:
        print("Program ran into an error.\n")
        sys.exit()

    return config
    # print("Configs: \n {}".format(config))






    # for index in range(len(in_ports)):
    # port = in_ports[index]

    # daemon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # daemon.bind(('localhost', portnum))
    # daemon.listen(1)

    # print("\nIncorrect header detected on line {} of config file.\n".format(Exception))

    # while True:
    ##use select() to block until events occur
    # pass
