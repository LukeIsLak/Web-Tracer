import socket
import ssl
import sys
import re

from URIHandler import parsedURI

def create_socket(hostname, port):
    """
    Given a website hostname and port number, create and return a socket.   

    If port number is 443, create a wrapped socket
    If port number is 80, create a unwrapped socket 
    """

    print('---Creating Socket---')
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        if port == 443:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=hostname)
        print('---Created Socket---')  
        return sock
    except Exception:
        print("---Error: Could Not Create Socket---")
        sys.exit()


def connect_socket(sock, pURI):
    """
    Given a socket and parsed URI, connects the socket to the host name and port number of the parsed URI.
    """

    print('---Connecting to Server---')
    try:
        sock.connect((pURI.getHost(), int(pURI.getPort())))
        print('---Connected to Server---')
    except socket.gaierror:
        print("---Error: Invalid URI Attempted - Potential Address or Port Info Error ---")
        sys.exit()
    except Exception:
        print("---Error: Connection to server failed---")
        sys.exit()

def sendHTTPMessage(sock, pURI):
    """
    Given a socket and parsed URI, creates an http_request to send to a web server.
    """

    http_request =  "GET /" + pURI.getFilePath() + " HTTP/1.1\r\nHost: " + pURI.getHost() + "\r\nConnection: close\r\n\r\n"

    print('---Sending a Message---\n')
    print('~~~~~HTTP REQUEST~~~~~~')
    print(http_request)
    print('~~~~~~~~~~~~~~~~~~~~~~~\n')

    try:
        sock.sendall(http_request.encode())
        print('---Message Sent---')
    except Exception:
        print("---Error: Could not send HTTP request---")
        sys.exit()

def recvHTTPMessage(sock):

    print('---Recieving A Message From The Server---')
    try:
        print('---Starting to Recieve Message---')
        response = b''
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                response += data
            except socket.timeout:
                print("---Warning: Recieving Message Timed Out - Using Gathered Message---")
                break
        if len(response) == 0:
            print('---Error: Recieved Message is Empty---')
            sys.exit()
        return splitResponseByte(response)[0].decode()
    except UnicodeDecodeError:
        print('---Error: Could not Decode Message---')
        sys.exit()
    except Exception as e:
        print("---Error: Could Not Retrieve From Server---")
        sys.exit()

def parseResponseCode(resp):
    try:
        parseResponse = int(resp.split("\r\n")[0].split(' ')[1])
        return parseResponse
    except Exception:
        print('---Error: Could Not Parse Response Code---')
        sys.exit()

def handleRedirect(resp, code, hostname, filepath):
    try:
        print('---Redirecting: Response Code of ' + str(code) + '---')
        parseRedirectURL = re.search(r'[L|l]ocation: (.*)', resp).group(1).replace('\r', '')

        if parseRedirectURL[0] == "/":
            if (len(filepath) != 0):
                parseRedirectURL = hostname + "/" + filepath + parseRedirectURL
            else:
                parseRedirectURL = hostname + parseRedirectURL
        print('---Redirected To: ' + parseRedirectURL + '---\n\n')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
        pURI = parsedURI(parseRedirectURL)
        recv = socket_handler(pURI)
        return (recv, pURI)
    except Exception:
        print('---Error: Could not parse Location from header---')
        sys.exit()


def splitResponseByte(resp):
    return resp.split(b'\r\n\r\n', 1)

def socket_handler(pURI):

    sock = create_socket(pURI.getHost(), pURI.getPort())
    connect_socket(sock, pURI)
    sendHTTPMessage(sock, pURI)
    recv = recvHTTPMessage(sock)
    print(recv)
    sock.close()

    return recv  

def handleUnauthorized(code):
    if code == 401:
        print('---Output: Is Password Protected? - Yes---')
    else:
        print('---Output: Is Not Password Protected? - No---')

def handleCookies(resp):
    print('---Output: Cookies - Printing All Cookies Below---')
    cookieRe = re.findall('[S|s]et-[C|c]ookie: (.*)', resp)
    
    for cookie in cookieRe:
        cookieName = "Cookie Name: " + re.search('^([^=]*)=', cookie).group(1)
        cookieExp = re.search('expires=([^;]*);', cookie)
        cookieDomain = re.search('domain=([^;]*);', cookie)

        cookieExp = '' if cookieExp == None else ", Expires: " + cookieExp.group(1)
        cookieDomain = '' if cookieDomain == None else ", Domain: " + cookieDomain.group(1)

        print(cookieName + cookieExp + cookieDomain)

def handleH2Check(pURI):
    try:
        context = ssl.create_default_context()
        context.set_alpn_protocols(['h2', 'http/1.1'])
        with socket.create_connection((pURI.getHost(), 443)) as sock:
            with context.wrap_socket(sock, server_hostname=pURI.getHost()) as ssl_sock:
                protocols = ssl_sock.selected_alpn_protocol()
                if protocols:
                    print('---Output: Supports H2? - YES---')
                else:
                    print('---Output: Supports H2? - NO---')
    except ssl.CertificateError as e:
        print('---Output: Supports H2 - NO---')
    except Exception as e:
        print('---Error: Could not check H2 protocol---')
        sys.exit()
    

def formatOutput(pURI: parsedURI):
    fullRecv = socket_handler(pURI)
    header = fullRecv
    respCode = parseResponseCode(header)
    newpURI = pURI

    while respCode == 302 or respCode == 301 or respCode == 307 or respCode == 308:
        handledRed = handleRedirect(header, respCode, pURI.getHost(), pURI.getFilePath())
        header = handledRed[0]
        newpURI = handledRed[1]
        respCode = parseResponseCode(header)

    print('---Output: Final Response Headers---')
    print(header + '\n')

    print('---Output: Final Additional Checks---')
    handleUnauthorized(respCode)
    handleH2Check(newpURI)
    handleCookies(header)
    print('---Output Complete: Everything was Successfull---')