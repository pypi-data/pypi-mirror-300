# -*- coding: utf-8 -*-
"""mywattsmon"""

import argparse
import json
import os
import sys
import time
import importlib
from queue import Queue
from threading import Thread
from threading import Lock

from mywattsmon.app.helper.dbwriter import DbWriter
from mywattsmon.app.helper.logger import Logger
from mywattsmon.app.helper.responder import Responder
from mywattsmon.app.helper.pathfinder import PathFinder
from mywattsmon.app.helper.timer import Timer

WAIT_SECONDS = 5

class Monitor:

    """
    Monitor class.
    """

    def __init__(self, datapath:str=None):
        """Setup.

        Args:
            datapath (str): This application's datapath, or None.

        Returns:
            None.
        """
        # Class name in lower case
        self.name = __class__.__name__.lower()

        # Path information
        pathinfo = PathFinder().get_pathinfo(datapath)
        configfile = pathinfo.get('configfile')
        datapath = pathinfo.get('datapath')

        # Configuration load
        with open(configfile, 'r') as f:
            self.config = json.load(f)
            
        # Listener port
        port = int(self.config['port'])

        # Logger
        loggerconfig = {}
        loggerconfig['datapath'] = datapath
        loggerconfig['loglevel'] = self.config['loglevel']
        loggerconfig['logtofile'] = self.config['logtofile']
        loggerconfig['logsource'] = self.name
        self.logger = Logger(loggerconfig)
        self.logger.log(0, f"Datapath: '{datapath}'")
        
        # Timer
        timerconfig = {}
        timerconfig['times'] = self.config['database']['times']
        self.timer = Timer(timerconfig)
        self.lasttime = ''
        
        # Database
        dbfile = f"{datapath}/db/monitor.db"
        tablename = self.config['database']['tablename']
        columns = self.config['database']['columns']
        self.dbwriter = DbWriter(dbfile, tablename, columns)
        self.logger.log(0, f"Database: '{dbfile}', table: '{tablename}'")
        
        # Put out listener port
        self.logger.log(0, f"Listener port: {port}")
        
         # Queues
        self.tasktrigger = Queue()
        self.taskqueues = {}

        # Threads
        self.threadlock = Lock()
        self.current_values = {}

        # Device threads
        for device in self.config['devices']:
            taskqueue = Queue()
            self.taskqueues[device] = taskqueue
            thread = Thread(target=self.__device, args=(device, taskqueue))
            thread.daemon = True
            thread.start()
            self.logger.log(0, f"{device} thread started.")

        # Wait for task thread
        thread = Thread(target=self.__wait_for_task, args=())
        thread.daemon = True
        thread.start()
        self.logger.log(0, "Wait for task thread started.")
        
        # Responder thread
        self.responder = Responder(port, self.tasktrigger, self.logger)
        thread = Thread(target=self.responder.listen, args=())
        thread.daemon = True
        thread.start()
        self.logger.log(0, "Responder thread started.")

        # Stop indicator
        self.stop = False
        
    def process(self):
        """The main monitor process.
        
        Can be stopped via KeyboardInterrupt, also under Windows.
         
        Args:
            None.
                   
        Returns:
            int: 0=regular, 1=irregular end of the process.
        """
        eop = 0
        try:
            while True:
                # Check stop indicator
                if self.stop is True:
                    break
                # Wait for next time to write
                t = self.timer.timematch()
                if t is not None and t != self.lasttime:
                    self.lasttime = t
                    # Get and write current data
                    data = self.__task()
                    if data is not None:
                        rowid = self.dbwriter.add_current_values(data)
                        self.logger.log(0, f"Row {rowid} added.")
                else:
                    # Wait a while
                    time.sleep(WAIT_SECONDS)
        except KeyboardInterrupt:
            self.logger.log(0, "Close request received.")
        except:
            eop = 1
            self.logger.log(1, "Error in monitor process.")
        finally:
            self.__close()
        self.logger.log(0, "End of monitor process. Bye")
        return eop
        
    def stop_process(self):
        """Sets the stop indicator to stop the main monitor process.
         
        Args:
           None.
        
        Returns:
           None
        """
        self.stop = True
        self.logger.log(0, "Stop indicator set.")
        
    # ---------------
    # Private methods
    # ---------------

    def __close(self):
        """Closes resources.
         
        Args:
           None.
        
        Returns:
           None
        """
        # Responder
        try:
            self.logger.log(0, "Closing responder ...")
            with self.threadlock:
                self.responder.close()
            time.sleep(0.5)
        except:
            self.logger.log(1, "Could not close responder.")
        # Task handler
        try:
            self.logger.log(0, "Closing task handler ...")
            with self.threadlock:
                self.tasktrigger.put('exit')
            time.sleep(0.5)
        except:
            self.logger.log(1, "Could not close task handler.")
        # Devices
        try:
            self.logger.log(0, "Closing devices ...")
            with self.threadlock:
                for device in self.taskqueues:
                    try:
                        self.taskqueues.get(device).put('exit')
                        time.sleep(0.5)
                    except:
                        self.logger.log(1, f"Could not close {device}.")
        except:
            self.logger.log(1, "Could not close devices.")

    def __wait_for_task(self):
        """Waits for tasks in an own thread.
         
        Args:
            None.
                   
        Returns:
            None.
        """
        while True:
            try:
                task = self.tasktrigger.get()
                if task == 'exit':
                    break
                self.responder.set_data(self.__task())
            finally:
                self.tasktrigger.task_done()
        self.logger.log(0, "Waiting for tasks stopped.")
        
    def __task(self):
        """Performs tasks in an own thread.
         
        Args:
            None.
                   
        Returns:
            dict: The result data of a task.
        """
        try:
            # Perform tasks
            for device in self.taskqueues:
                self.taskqueues.get(device).put('do')
            for device in self.taskqueues:
                self.taskqueues.get(device).join()
            # Return data
            return self.current_values.copy()
        except:
            self.logger.log(1, "Error when performing a task.")
        return None
 
    def __device(self, device:str, taskqueue:object):
        """Handles a device class instance in an own thread.

        Args:
           device (str): Simple device class name, e.g. Fritz.
           taskqueue (object): Queue to receive a task.
        
        Returns:
           None.
        """
        instance = self.__get_instance(device)
        while True:
            try:
                task = taskqueue.get()
                infoset = {}
                if task == 'exit':
                    instance.close()
                    self.logger.log(0, f"Instance of {device} closed.")
                    break;
                elif task != 'do':
                    self.logger.log(2, f"Unknown task '{task}'.")
                else:
                    infoset = instance.get_infoset()
                    for unit in infoset:
                        values = {}
                        values['power'] = infoset[unit].get('power')
                        values['energy'] = infoset[unit].get('energy')
                        values['state'] = infoset[unit].get('state')
                        values['code'] = infoset[unit].get('code')
                        values['info'] = infoset[unit].get('info')
                        if values['code'] == 1:
                            self.logger.log(1,
                                f"Error at {device}, unit {unit}: " \
                                f"{infoset[unit].get('trace')}"
                                )
                        values['trace'] = ''
                        with self.threadlock:
                            self.current_values[unit] = values
            except:
                self.logger.log(1, f"Error at {device}.")
            finally:
                taskqueue.task_done()

    def __get_instance(self, device:str):
        """Gets a device class instance by device class name.
         
        Args:
           device (str): A simple device class name, e.g. Fritz.

        Returns:
           object: Instance of the device class.
        """
        module = self.config['devices'][device]['module']
        clazz = getattr(importlib.import_module(module), device)
        instance = clazz()
        instance.set_config(self.config['devices'][device])
        self.logger.log(0, f"Instance of {device} created.")
        return instance
      
# ----
# Main
# ----

def main(args):
    parser = argparse.ArgumentParser(
    description="MONITOR process.",
    usage="python -m mywattsmon.app.monitor [-h,--help] [-d,--datapath]")
    parser.add_argument('-d', '--datapath', type=str,
        default="mywattsmon-data",
        help="e.g. 'mywattsmon-data', or an absolute path")
    args = parser.parse_args()
    print("  ===================================")
    print("  MONITOR process. Close with Ctrl+C.")
    print("  ===================================")
    monitor = Monitor(args.datapath)
    return monitor.process()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
