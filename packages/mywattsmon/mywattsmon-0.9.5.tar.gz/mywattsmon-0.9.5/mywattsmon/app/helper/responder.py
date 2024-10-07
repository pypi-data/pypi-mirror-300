# -*- coding: utf-8 -*-
"""mywattsmon"""

import json
import socket
import time
from queue import Queue
from threading import Thread
from threading import Lock

LOCALHOST = '127.0.0.1' # Localhost IPv4 address
DATALENGTH = 1024*8     # Data length maximum
SOCKTIMEOUT = 5         # Listener socket timeout seconds

class Responder:

    """
    Responder class.
    """

    def __init__(self, port:int, tasktrigger:object, logger:object):
        """Setup.

        Args:
            port (int): The port number on localhost.
            tasktrigger (object): Queue to trigger request processing.
            logger (object): The logger instance to use.

        Returns:
            None.
        """
        self.port = port
        self.tasktrigger = tasktrigger
        self.logger = logger
        self.threadlock = Lock()
        self.stoptrigger = Queue()
        self.data = None

    def set_data(self, data:dict):
        """Sets the current data.
        
        Args:
           data (dict): The data.
                   
        Returns:
           None.
        """
        with self.threadlock:
            self.data = data

    def listen(self):
        """Listens for requests.
        
        Socket shutdown is not performed due to Windows.

        Args:
           None.
                   
        Returns:
           None.
        """
        lsock = None # Listener socket
        socks = [] # Requester sockets
        try:
            lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lsock.settimeout(SOCKTIMEOUT)
            lsock.bind((LOCALHOST, self.port))
            lsock.listen()
            while True:
                try:
                    sock, addr = lsock.accept()
                except socket.timeout:
                    if not self.stoptrigger.empty():
                        self.stoptrigger.task_done()
                        break
                    else:
                        continue
                self.logger.log(0, f"New requester thread {addr}.")
                socks.append({'sock':sock, 'addr':addr})
                thread = Thread(target=self.__requester, args=(sock, addr))
                thread.daemon = True
                thread.start()
        except:
            self.logger.log(1, "Error while listening.")
        finally:
            for sock in socks:
                try:
                    fd = sock['sock'].fileno()
                    if fd > -1 :
                        self.logger.log(0, f"Closing socket " \
                                           f"{sock['addr']} ...")
                        #sock['sock'].shutdown(socket.SHUT_RDWR)
                        sock['sock'].close()
                        self.logger.log(0, "Socket closed.")
                except:
                    self.logger.log(1, f"Could not close socket " \
                                       f"{sock['addr']}.")
            try:
                if lsock:
                    fd = lsock.fileno()
                    if fd > -1:
                        self.logger.log(0, "Closing listener socket ...")
                        #lsock.shutdown(socket.SHUT_RDWR)
                        lsock.close()
                        self.logger.log(0, "Listener socket closed.")
            except:
                self.logger.log(1, "Could not close listener socket.")

    def close(self):
        """Sets the stop indicator.

        Args:
           None.
                   
        Returns:
           None.
        """
        self.logger.log(0, "Listener stop requested ...")
        self.stoptrigger.put('stop')
        self.stoptrigger.join()
        self.logger.log(0, "Listener stop commited.")
        
    # ---------------
    # Private methods
    # ---------------
    
    def __get_data(self):
        """Gets the current data in the form required for response.

        Args:
           None
                   
        Returns:
           bytes: The data to be sent as response.
        """
        data = None
        try:
            with self.threadlock:
                data = self.data.copy()
            data = json.dumps(data)
            data = bytes(data, encoding='utf-8')
        except:
            self.logger.log(1, "Invalid data.")
            data = bytes(json.dumps({}), encoding='utf-8')
        return data
        
        
    def __requester(self, sock:object, addr:tuple):
        """Handles requests for a specific requester in an own thread.
         
        Args:
           sock (object): The requester socket.
           addr (tuple): The requester address.
                   
        Returns:
           None.
        """
        reqid = None
        try:
            while True:
                data = sock.recv(DATALENGTH)
                try:
                    if not data:
                        break
                except ConnectionAbortedError:
                    break
                except ConnectionRefusedError:
                    break
                except ConnectionError:
                    break
                try:
                    reqid = data.decode('utf-8')
                    reqaddr = f"{addr[0]}:{str(addr[1])}"
                    # -----------------------------------------
                    if reqid != reqaddr:
                        warning = f"Requester ID missmatch: " \
                            f"Requester ID is {reqid}, " \
                            f"but address is {reqaddr}."
                        self.logger.log(2, warning)
                    # -----------------------------------------
                    self.tasktrigger.put('do')
                    self.tasktrigger.join()
                finally:
                    sock.sendall(self.__get_data())
        except:
            self.logger.log(1, f"Could not handle request for {addr}.")
        finally:
            try:
                fd = sock.fileno()
                if fd > -1:
                    self.logger.log(0, f"Closing socket {addr} ...")
                    #sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                    self.logger.log(0, "Socket closed.")
            except:
                self.logger.log(1, "Could not close socket.")
 
