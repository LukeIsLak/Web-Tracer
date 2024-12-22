FILES

    WebTester.py - Handles the User Input
    URIHandler.py - Handles the parsing of the URI
    SocketHandler.py - Handles the socket and related functions, handles the outputs


---------------------------------------------------

COMPILATION / USAGE

    In the directory of the project
    1) open a bash terminal
    2) go to the directory where WebTester.py, SocketHandler.py, and URIHandler are kept
    2) run this command into the terminal.

    ```
    python WebTester.py [URI]
    ```

    Example Input
    ```
    python WebTester.py https://www.google.ca
    ```

    NOTE: WebTester.py is looking for a URI as a system argument, if additional arguments are passed they will be ingored.
    If no inputs are passes the program will terminate with a custom error.

    --- URI Properties ---
    WebTester.py accpets the following types of inputs
    - http://example.com/path
    - https://www.example.com/path
    - example.com/
    - example.com
    - www.example.com
    - www.example.com[:port number]

    NOTE: WebTester.py uses URIHandler.py to parse URI's, if no protocol is detected, https is automatically assumed.
    NOTE: URI's that are outside of the accepted inputs will be handled by URIHandler.py, but will exit the program with a custom error status

---------------------------------------------------

OUTPUT

    The program outputs the following
    1) Whether or not the server is password protected
    2) Whether or not the server supports http2
    3) A list of the servers cookies
        - If cookies include a domain server or expiry date, that is also included


    Additionally, the program outputs the current status of the program, for example, a potential output could be the following