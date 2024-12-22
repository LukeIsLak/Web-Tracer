import re
import sys

class parsedURI:
    """
    Class that handles the parsing of a string. Returns a class of a parsed URI.

    Converts any URI passed into it into 4 components: a protocol, a hostname, a port number, and a filepath.
    Class returns contains getter functions to collect each component. 
    """

    def __init__(self, uri: str):
        """
        Initialize and create a class that turns a URI into a parsed, tokenized, class of URI components
        """
        self._prot = parseProtocol(uri)
        self._host = parseHost(uri)
        self._port = parsePort(uri, self._prot)
        self._filepath = parseFilePath(uri)

        print('---Parsed URI---\n')
        print('~~~~URI Components~~~~')
        print(self)
        print('~~~~~~~~~~~~~~~~~~~~~~\n')

    def getProt(self):
        """
        Returns the URI protocol
        """

        return self._prot
    def getHost(self):
        """
        Returns the URI hostname
        """
        
        return self._host
    def getPort(self):
        """
        Returns the URI port number
        """
        
        return self._port
    def getFilePath(self):
        """
        Returns the URI filepath
        """
        
        return self._filepath
    
    def __str__(self) -> str:
        """
        Defines how to parse this class into a string
        """
        
        return "Protocol: " + str(self._prot) + "\nHost: " + str(self._host) + "\nPort: " + str(self._port) + "\nFile Path: " + str(self._filepath)
    
def parseProtocol(url:str) -> str:
    """
    Given a URI, returns the protocol of it as a string

    Only recognizes 'http' and 'https' as protocols
    If there is no potocol detected, throws an Error
    """

    try:
        re_protocol = re.match(r'^([^:\/]+):\/\/', url)
        prot = re_protocol.group(1)
        if prot != "http" and prot != "https":
            print("---Error: Parsing URI - Invalid Protocol---")
            sys.exit()
        return prot
    except AttributeError:
        print("---Warning: No Protocol Detected: Using HTTPS---")
        return "https"
    except Exception:
        print("---Error: Parsing URI - Parsing Protocol---")
        sys.exit()

def parseHost(url:str) -> str:
    """
    Given a URI, returns the host name of it as a string

    If there is no host name detected, throws an Error
    """

    try:
        re_host = re.match(r'^[^:\/]+:\/\/([^:\/]+)', url)
        host = re_host.group(1)
        return(host)

    except AttributeError:
        try:
            re_host = re.match(r'^([^:\/]+)', url)
            host = re_host.group(1)
            return(host)
        except AttributeError:
            print("---Error: No Host---")
            sys.exit()
    except Exception:
        print("---Error: Parsing URI - Parsing Host Name---")
        sys.exit()

def parsePort(url: str, protocol: str) -> int:
    """
    Given a URI, returns the port number of it as a int

    If there is no port number detected, returns 443 if the protocol is 'https', otherwise 80
    """

    try:
        re_port = re.match(r'^.+:\/\/.+:+(\d+)\/?.+', url)

        if re_port == None:
            return (80 if  protocol == 'http' else 443)
            
        port = re_port.group(1)
        return(port)
    except Exception:
        print("---Error: Parsing URI - Parsing Port---")
        sys.exit()

def parseFilePath(url: str) -> str:
    """
    Given a URI, returns the filename of it as a string

    If there is no filename detected, return an empty string
    """
    try:
        re_filepath = url.replace('//', '').split('/', 1)
        return re_filepath[1] if len(re_filepath) == 2 else  ''
    except Exception:
        print("---Error: Parsing URI - Parsing File Path")
        sys.exit()
