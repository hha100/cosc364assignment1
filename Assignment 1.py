import sys, socket, select

class IncorrectConfigHeader(Exception):
    """Raised when the leftmost word of a line in the config file is not a recognised header"""
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

router_id = 0
in_ports = []
out_ports = []
timer = 180

try:
    for line in config_lines:
        if line[0] == 'router-id':
            pass
        elif line[0] == 'input-port':
            pass
        elif line[0] == 'output-port':
            pass
        elif line[0] == int(line[0]) and int(line[0]) in range():
            pass
        else:
            raise IncorrectConfigHeader
except IncorrectConfigHeader:
    pass
except:
    print("Unknown error occured while processing config file. Please double check that values used are correct\n")
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
