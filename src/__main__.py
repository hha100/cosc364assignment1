"""
__main__.py is run by default when naming the directory in the command line, meaning you don't need to specify
which file you want to run
e.g. 'py src conf/config1.txt'
"""

import daemon, sys

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

    # Do the main loop of the routing daemon here after config file parsed, routers initialised, and initial routing table populated.
    dae = daemon.Daemon()
    dae.start_loop(config_filename)

if __name__ == "__main__":
    main()
