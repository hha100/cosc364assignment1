"""
COSC364 Assignment 1
RIP Routing

Authors: Henry Hay-Smith and Ryan Akers
Date: 27/04/2021

__main__.py is run by default when naming the directory in the command line, meaning you don't need to specify
which file you want to run
e.g. 'py src conf/config1.txt'
"""

import daemon, sys

def main():
    """ Starts the program by reading config file and beginning infinity loop"""
    
    # If there is a command line argument, save it as the config filename
    if len(sys.argv) > 1:
        config_filename = str(sys.argv[1])
    
    # If there is no command line argument, print an error message and exit
    else:
        print("\nConfig filename not detected. Please use a command line argument of the form 'router1_config.txt'.\n")
        sys.exit()  # Exit the program with an error message if there is no command line argument
    
    # To aid with readability of the text output in terminal
    print()

    # Create an instance of the Daemon class for the routing daemon and enter the infinite loop
    dae = daemon.Daemon()
    dae.start_loop(config_filename)

# Statement to run the main function above automatically
if __name__ == "__main__":
    main()
