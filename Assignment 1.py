import sys, socket, select

class IncorrectConfigHeader(Exception):
    """Raised when the leftmost word of a line in the config file is not a recognised header"""
    pass

class RouterIDError(Exception):
    """Raised when the router id is not an integer or is out of the range 1 -> 64000"""
    pass

class PortDupeError(Exception):
    """Raised when the config file contains a duplicate port number"""
    pass

prog_name = sys.argv[0]
print()

if len(sys.argv) > 1:
    config_filename = str(sys.argv[1])
else:
    print("Config filename not detected. Please use a command line argument of the form 'router1_config.txt'.\n")
    sys.exit()

try:
    file = open(config_filename, 'r')
    config_lines = file.readlines()
    file.close()
except:
    print("File could not be found.\n")
    sys.exit()

try:
    for index in range(len(config_lines)):
        config_lines[index] = [x.strip('\n') for x in config_lines[index].split(' ')]
except:
    print("Incorrect header detected on line {} of config file.\n".format(index))
    sys.exit()

print(config_lines)

router_id = -1
input_ports = []
output_ports = []
timer = 180

try:
    for line in config_lines:
        print("LINE IS:", line)
        first = line[0]
        if first == 'router-id':
            print('1\n')
            
            if router_id == -1 and line[1] in range(1, 64001):
                router_id = line[0]
                print("Router ID assigned correctly\n")
            else:
                raise RouterIDError
            
        elif first == 'input-ports':
            print('2\n')
            if line[1] in input_ports or line[1] in output_ports:
                raise PortError
            
            elif type(line[1]) == type(0) and line[1] in range(1024, 64001):
                pass
            
        elif first == 'output-ports':
            print('3\n')
            
        elif first == 'timer':
            #if line[1] == int(line[0]) and int(line[0]) in range()
            timer = line[1]
            print('4\n')
            
        else:
            raise IncorrectConfigHeader
        
except IncorrectConfigHeader:
    print("One of the headers in the config file cannot be processed. Make sure that the header is one of the following:\nrouter-id, input-port, output-port, timer\n")
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

while True:
    #use select() to block until events occur
    pass
