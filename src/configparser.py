import sys

def parse(config_filename):
    """ Attempts to open file given in a command line argument and read router parameters."""
    
    # To aid with readability of the text output in terminal
    print()
    
    # Try to open the file, save the lines in a list, and close the file
    try:
        file = open(config_filename, 'r')
        config_lines = file.readlines()
        file.close()
    
    # If the file can't be found and/or read, exit the program with an error message
    except:
        print("File could not be found or is not a readable .txt file.\n")
        sys.exit()
    
    # Split each line into strings and strip any newline characters
    try:
        for index in range(len(config_lines)):
            config_lines[index] = [x.strip("\n") for x in config_lines[index].split(" ")]
    
    # Exit the program with an error message if there is a line in the config file that cannot be split into strings
    except:
        print("Incorrect line format on line {} of config file.\n".format(index))
        sys.exit()
    
    # Initialise the router parameters as empty variables and set the default timer intervals to 180 seconds for timeout and 30 seconds for periodic
    router_id = None
    input_ports = []
    output_ports = []
    timeouts = [180, 30]

    # Try to read all lines from the config file
    try:
        
        # For each line in the config file
        for line in config_lines:
            
            # Take the line header as a separate variable
            first_str = line[0]

            # If the line being read is assigning the router ID
            if first_str == "router-id":
                
                # If the router ID has not yet been set
                if router_id == None:
                    
                    # If the router ID is not a positive integer, print an error message and exit
                    if line[1].isnumeric() == False:
                        print("Router ID must be a positive integer.\n")
                        sys.exit()
                        
                    # If the router ID is not between 1 and 64000, print an error message and exit
                    if int(line[1]) not in range(1, 64001):
                        print("Router ID must be between 1 and 64000.")
                        sys.exit()
                        
                    # If the router ID is a positive integer between 1 and 64000, assign it to the router_id variable
                    else:
                        router_id = int(line[1])
                        print("Router ID assigned to {}\n".format(router_id))
                        
                # If the router ID has already been assigned, print an error message and exit
                else:
                    print("Router ID must only be assigned once.\n")
                    sys.exit()

            # If the line being read is assigning the input ports
            elif first_str == "input-ports":
                
                # For each value following the header string
                for index in range(1, len(line)):
                    
                    # If the value is not a positive integer, print an error message and exit
                    if line[index].isnumeric() == False:
                        print("ERROR: Input ports must be positive integers.\n")
                        sys.exit()
                        
                    # If the value is already assigned as an input port, print an error message and exit
                    elif int(line[index]) in input_ports:
                        print("ERROR: Duplicate input port number detected.\n")
                        sys.exit()
                        
                    # If the value is already assigned as an output port, print an error message and exit
                    elif int(line[index]) in [x[0] for x in output_ports]:
                        print("ERROR: An input port is already assigned as an output port.\n")
                        sys.exit()
                        
                    # If the value is not between 1024 and 64000, print an error message and exit
                    elif int(line[index]) not in range(1024, 64001):
                        print("ERROR: All input ports in the config file must be between 1024 and 64000\n")
                        sys.exit()
                    # If the port number has not already been assigned and is a positive integer between 1024 and 64000, append it to the input_ports list
                    else:
                        input_ports.append(int(line[index]))
                # Print a list of the input ports assigned by this line of the config file
                print("Input ports assigned to {}\n".format([x for x in input_ports]))

            # If the line being read is assigning the output ports
            elif first_str == "output-ports":
                
                # For each set of values after the header string
                for index in range(1, len(line)):
                    
                    # Split the set of values separated by hyphens into a list of values
                    output = line[index].split("-")
                    
                    # If the length of one of the lists of values is not 3 as expected, print an error message and exit
                    if len(output) != 3:
                        print("ERROR: The length of an output port definition is of incorrect length. Make sure output ports are of the form PORT-METRIC-ROUTER ID.\n")
                        sys.exit()
                    
                    # If any of the values in the list are not positive integers, print an error message and exit
                    elif output[0].isnumeric() == False or output[1].isnumeric() == False or output[2].isnumeric() == False:
                        print("ERROR: Output ports, metrics and router IDs must be positive integers.\n")
                        sys.exit()
                    
                    # If the port number is already assigned as an input port, print an error message and exit
                    elif int(output[0]) in input_ports:
                        print("ERROR: An output port is already assigned as an input port.\n")
                        sys.exit()
                    
                    # If the port number is already assigned as an output port, print an error message and exit
                    elif int(output[0]) in [x[0] for x in output_ports]:
                        print("ERROR: Duplicate output port number detected.\n")
                        sys.exit()
                    
                    # If the port number is not between 1024 and 64000, print an error message and exit
                    elif int(output[0]) not in range(1024, 64001):
                        print("ERROR: All output ports in the config file must be between 1024 and 64000\n")
                        sys.exit()
                    
                    # If the destination router of the output port matches this routers ID number, print an error message and exit
                    elif int(output[2]) == router_id:
                        print("ERROR: The router ID of one of the output ports matches the router ID of this router.\n")
                        sys.exit()
                    
                    # If the destination router ID is not between 1 and 64000, print an error message and exit
                    elif int(output[2]) not in range(1, 64001):
                        print("ERROR: The router ID of one of the output ports is not between 1 and 64000.\n")
                        sys.exit()
                    
                    # If all of the output ports values are correct, append a list containing them to the output_ports list
                    else:
                        output_ports.append([int(x) for x in output])
                
                # Print a series of messages confirming the assignment of all output ports
                print("Output ports assigned to {}".format([x[0] for x in output_ports]))
                print("Output metrics assigned to {}".format([x[1] for x in output_ports]))
                print("Output router IDs assigned to {}\n".format([x[2] for x in output_ports]))

            # If the line being read is assigning the timeout interval
            elif first_str == "timeout":
                
                # If the timeout interval is not a positive integer, print an error message and exit
                if line[1].isnumeric() == False:
                    print("ERROR: Timeout value is not a positive integer.\n")
                    sys.exit()
                
                # If the timout interval is valid, use integer division by a factor of 6 to get the periodic timer interval
                else:
                    timeouts[0] = int(line[1])
                    timeouts[1] = int(timeouts[0] / 6)
                
                # Print a message confirming the timer intervals
                print("Timeout and periodic timer intervals are assigned to {} seconds and {} seconds\n".format(timeouts[0], timeouts[1]))

        # Create an empty error message to give if any of the mandatory router parameters (router ID, input ports, and output ports) have not been set
        error_msg = ""
        
        # If the router ID has not been set, add a statement to the error message
        if router_id == None:
            error_msg += "ERROR: Router ID was not assigned in config file.\n"
        
        # If the input ports have not been set, add a statement to the error message
        if input_ports == list():
            error_msg += "ERROR: Input ports not assigned in config file.\n"
        
        # If the output ports have not been set, add a statement to the error message
        if output_ports == list():
            error_msg += "ERROR: Output ports not assigned in config file.\n"
        
        # If the error message is not empty (i.e. if any of the mandatory  router parameters has not been set), print an error message and exit
        if error_msg != "":
            print(error_msg)
            sys.exit()

    # If any error occurs while reading config file parameters, print an error message and exit
    except:
        print("Program ran into an error while reading the configuration file.\n")
        sys.exit()
    
    # If values have been read correctly, have the function return them separately
    return config_filename, router_id, input_ports, output_ports, timeouts