import sys

prog_name = sys.argv[0]
if len(sys.argv) > 1:
    config_filename = str(sys.argv[1])
else:
    print("\nConfig filename not detected. Please use a command line argument of the form 'router1_config.txt'.\n")
    sys.exit()

try:
    file = open(config_filename, 'r')
    config_lines = file.readlines()
    file.close()
except:
    print("\nFile could not be found.\n")
    sys.exit()
    
print(config_lines)

try:
    for index in range(config_lines):
        config_lines[index] = config_lines[index].split(' ')
except:
    pass