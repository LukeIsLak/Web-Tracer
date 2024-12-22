import sys
import socket
import ssl

from SocketHandler import *
from URIHandler import *


def initialize():
    """
    Initializes the program.

    Collects arguements from the standard input, and begins the Smart Client program.
    Accepts 2 arguements from the standard input
        1) file initialization
        2) Any URI
    
    Any additional arguements will be ignored
    """


    inputs = sys.argv

    #Exit program if there is no URI
    if len(inputs) == 1:
        print('---Initialization Failed: No arguement passed through---')
        sys.exit()

    #Warn user if there is more arguements than required
    if len(inputs) > 2:
        print('---Initialization Warning: Only applies first argument passed---')
    
    print('---Initializing: Starting SmartClient with an input of ' + sys.argv[1] + '---')
    pURI = parsedURI(sys.argv[1])
    formatOutput(pURI)


if __name__ == '__main__':
    initialize()