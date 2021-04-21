import sys, socket, select

#Custom errors for use with try/except
class IncorrectConfigHeader(Exception):
    """Raised when the leftmost word of a line in the config file is not a recognised header"""
    pass

class RouterIDError(Exception):
    """Raised when the router id is not an integer or is out of the range 1 -> 64000"""
    pass

class PortDupeError(Exception):
    """Raised when the config file contains a duplicate port number"""
    pass

class EmptyConfigError(Exception):
    """Raised when a line of the config file has a header but no value"""
    pass

print() #To aid with readability of the text output in terminal

if len(sys.argv) > 1:   #If there is a command line argument
    config_filename = str(sys.argv[1])  #Save the name of the config file for this router to a variable
else:
    print("Config filename not detected. Please use a command line argument of the form 'router1_config.txt'.\n")
    sys.exit()  #Exit the program with an error message if there is no command line argument

try:
    file = open(config_filename, 'r')   #Try to open the file
    config_lines = file.readlines()     #Save the lines from the config file in a list
    file.close()                        #Close the file
except:
    print("File could not be found or is not a readable .txt file.\n")
    sys.exit()  #If the file can't be found and/or read, exit the program with an error message

try:
    for index in range(len(config_lines)):
        config_lines[index] = [x.strip('\n') for x in config_lines[index].split(' ')]   #Split each line into strings and strip any newline characters
except:
    print("Incorrect line format on line {} of config file.\n".format(index))
    sys.exit()  #Exit the program with an error message if there is a line in the config file that cannot be split into strings

router_id = -1      #Set the router id to -1 initially so that it is possible to check if the router id has already been assigned to a correct value (between 1 and 64000)
input_ports = []    #Create an empty list to hold the input ports of this router
output_ports = []   #Create an empty list to hold the output ports of this router
timer = 1010         #Set the default timer interval to _____ ~~~~~(find a good default value later)~~~~~

try:
    for line in config_lines:
        if len(line) < 2:
            raise EmptyConfigError
        
        print("~~~~~~~~~ LINE IS:", line, "~~~~~~~~~")
        first_str = line[0]
        
        #If the line being read is assigning the router ID
        if first_str == 'router-id':
            
            if router_id == -1 and int(line[1]) in range(1, 64001):
                router_id = line[1]
                print("Router ID assigned to {}\n".format(router_id))
            else:
                raise RouterIDError
            
        #If the line being read is assigning the input ports
        elif first_str == 'input-ports':
            for index in range(1, len(line)):
                if line[index] in input_ports or line[index] in output_ports:
                    raise PortError
            
                elif line[index].isnumeric() and int(line[index]) in range(1024, 64001):
                    input_ports.append(line[index])
            
            print('Input ports assigned to {}\n'.format([x for x in input_ports]))
        
        #If the line being read is assigning the output ports
        elif first_str == 'output-ports':
            for index in range(1, len(line)):
                output_port = [x.strip('\n') for x in line[index].split('-')]
                print("-=-=-=-=-=-=-=- Port is:", output_port, "-=-=-=-=-=-=-=-")
            print('Output ports assigned to {}\n'.format([x for x in output_ports]))
        
        #If the line being read is assigning the timer interval
        elif first_str == 'timer':
            timer = line[1]
            print('TIMER IS: {}\n'.format(timer))    #FOR DEBUGGING
            
        else:
            raise IncorrectConfigHeader
        
except IncorrectConfigHeader:
    print("One of the headers in the config file cannot be processed. Make sure that the header is one of the following:\nrouter-id, input-ports, output-ports, timer\n")
    sys.exit()
    
except RouterIDError:
    print("\n")
    sys.exit()
    
except:
    print("Unknown error occured while processing config file. Please double check that each header is followed by a \n")
    sys.exit()

#for index in range(len(in_ports)):
    #port = in_ports[index]
    
    #daemon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #daemon.bind(('localhost', portnum))
    #daemon.listen(1)


#print("\nIncorrect header detected on line {} of config file.\n".format(Exception))

#while True:
    ##use select() to block until events occur
    #pass