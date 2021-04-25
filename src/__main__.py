"""__main__.py is run by default when naming the directory in the command line, meaning you don't need to specify
which file you want to run
e.g. 'py src conf/config1.txt' """

import routingtable, configparser, sys

if len(sys.argv) > 1:  # If there is a command line argument
    """config_filename = str(sys.argv[1])  # Save the name of the config file for this router to a variable"""
    config_filename = str(sys.argv[1])
else:
    print("\nConfig filename not detected. Please use a command line argument of the form 'router1_config.txt'.\n")
    sys.exit()  # Exit the program with an error message if there is no command line argument

configparser.parse(config_filename)
initialiserouters.init()