# -*- coding: utf-8 -*-
"""mywattsmon"""

import time
import traceback

LEVEL_ERROR = 'error'
LEVEL_WARNING = 'warning'
LEVEL_INFO = 'info'
LEVEL_TEST = 'test'

class Logger:

    """
    Logger class.
    """

    def __init__(self, config:dict):
        """Setup.

        Args:
            config (dict): Specific logger configuration.

        Returns:
            None.
        """
        self.loglevel = str(config['loglevel']).lower()
        self.logfile = None
        self.logtofile = False
        if config['logtofile'].lower() == 'true':
            self.logtofile = True
            logfilepath = f"{config['datapath']}/log"
            logsource = config['logsource']
            d = time.strftime("%Y-%m-%d", time.localtime())
            self.logfile = f"{logfilepath}/{logsource}-{d}.log"
            
    def get_logfilepath(self):
        """Gets the logfile path.
         
        Args:
           None.
        
        Returns:
           str: The absolute path to the logfile.
        """
        return self.logfile

    def log(self, code:int, message:str):
        """Logs information.
         
        Args:
           code (int): 0=OK, 1=error, 2=warning, 3=test.
           message (str): Message text.
        
        Returns:
           None.
        """
        if (self.loglevel == LEVEL_ERROR and code not in (1)) or \
           (self.loglevel == LEVEL_WARNING and code not in (1, 2)) or \
           (self.loglevel == LEVEL_INFO and code not in (0, 1, 2)):
            return
        trace = ''
        if code == 1:
            trace = " ".join(str(traceback.format_exc()).split())
            if trace.startswith("NoneType"):
                trace = ''
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logmessage = (f"{ts} {code}: {message} {trace}").strip()
        if self.logtofile is True:
            with open(self.logfile, "a") as f:
                f.write(f"{logmessage}\n")
        else:
            print(logmessage)
