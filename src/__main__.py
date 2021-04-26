"""__main__.py is run by default when naming the directory in the command line, meaning you don't need to specify
which file you want to run
e.g. 'py src conf/config1.txt' """

import routingtable
import configparser
import sys


def main():
    """
    Main code to be run
    """
    config_filename = str(sys.argv[1])
    config = configparser.parse(config_filename)
    print("Config: \n {0}".format(config))


if __name__ == "__main__":
    main()
