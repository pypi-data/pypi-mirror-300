# -*- coding: utf-8 -*-
"""mywattsmon"""

import socket
import json

LOCALHOST = '127.0.0.1' # Localhost IPv4 address
DATALENGTH = 1024*8     # Data length maximum

class Requester:

    """
    Requester class.
    """

    def __init__(self, port:int, logger:object):
        """Setup.

        Args:
            port (int): The port number on localhost.
            logger (object): The logger instance to use.

        Returns:
            None.
        """
        self.port = port
        self.logger = logger
        self.sock = None
        self.lhost = None
        self.lport = None
        self.rhost = None
        self.rport = None
        self.reqid = None

    def request(self):
        """Processes a request.
                 
        Args:
           None.
                   
        Returns:
           dict: Response data.
        """
        response = None
        try:
            if self.__open() is True:
                self.sock.sendall(bytes(self.reqid, encoding='utf-8'))
                data = self.sock.recv(DATALENGTH)
                if not data:
                    self.logger.log(2, f"{self.reqid}: No response data.")
                    self.sock = None
                else:
                    try:
                        response = json.loads(data.decode('utf-8'))
                    except:
                        self.logger.log(1, f"{self.reqid}: " \
                                           f"Invalid response.")
        except BrokenPipeError:
            self.logger.log(1, f"{self.reqid}: Connection broken.")
            self.sock = None
        except:
            self.logger.log(1, f"{self.reqid}: Could not handle request.")
            self.close()
        return response

    def close(self):
        """Closes the socket.
        
        Socket shutdown is not performed due to Windows.
                 
        Args:
           None.
                   
        Returns:
           None.
        """
        if self.sock:
            try:
                #self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                self.logger.log(0, f"{self.reqid}: " \
                                   f"Requester socket closed.")
            except:
                self.logger.log(2, f"{self.reqid}: " \
                                   f"Could not close requester socket.")
            self.sock = None
            
    # ---------------
    # Private methods
    # ---------------
            
    def __open(self):
        """Opens a socket if not yet done.
                 
        Args:
           None.
                   
        Returns:
           bool: True if the socket is open, else False.
        """
        try:
            if self.sock:
                return True # Already open
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((LOCALHOST, self.port))
            self.lhost = self.sock.getsockname()[0]
            self.lport = self.sock.getsockname()[1]
            self.rhost = self.sock.getpeername()[0]
            self.rport = self.sock.getpeername()[1]
            self.reqid = f"{self.lhost}:{str(self.lport)}"
            self.logger.log(0, f"Socket opened (" \
                        f"local {self.lhost}:{self.lport}, " \
                        f"remote {self.rhost}:{self.rport}).")
            return True
        except ConnectionRefusedError:
            self.logger.log(2, f"{self.reqid}: Connection refused. " \
                        f"The request destination appears to be " \
                        f"offline or unavailable.")
            self.sock = None
            return False
        except:
            self.logger.log(1, f"{self.reqid}: Could not open socket.")
            self.sock = None
            return False
