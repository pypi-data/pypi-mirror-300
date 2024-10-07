# -*- coding: utf-8 -*-
"""mywattsmon"""

import unittest
import json
import os
import time
import tkinter as tk
from queue import Queue
from threading import Thread

from mywattsmon.app.device.mock import Mock
from mywattsmon.app.helper.dbreader import DbReader
from mywattsmon.app.helper.dbwriter import DbWriter
from mywattsmon.app.helper.fontscaler import FontScaler
from mywattsmon.app.helper.logger import Logger
from mywattsmon.app.helper.pathfinder import PathFinder
from mywattsmon.app.helper.responder import Responder
from mywattsmon.app.helper.requester import Requester
from mywattsmon.app.helper.timer import Timer

APPLICATION_NAME = "mywattsmon"
CONFIGFILE_NAME = "config.json"
TEST_DATAPATH = "mywattsmon/test/data"

class AppTest(unittest.TestCase):
    
    """
    AppTest class - derived from unittest.TestCase.
    """
    
    def test_01_pathfinder(self):
        """Test for class PathFinder.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("-------------------------")
        print("Test for class PathFinder")
        print("-------------------------")
        
        # PathFinder
        pathfinder = PathFinder()
        
        # Path info
        pathinfo = pathfinder.get_pathinfo(TEST_DATAPATH)
        print("Path info:")
        for entry in pathinfo:
            print(f"{entry}: {pathinfo.get(entry)}")
        self.assertIsNotNone(pathinfo)
        
    def test_02_logger(self):
        """Test for class Logger.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("---------------------")
        print("Test for class Logger")
        print("---------------------")

        # Logger
        logger = self.get_logger()
        
        # Log to file
        logfile = logger.get_logfilepath()
        print(f"Logfile: {logfile}")
        logger.log(0, "Info")
        logger.log(1, "Error")
        logger.log(2, "Warning")
        logger.log(3, "Test") # Must not be written, loglevel is info

        # Read logfile and check the entries
        lines = self.get_loglines(logfile)
        for line in lines:
            print(line)
        self.assertIn("Info", lines[0])
        self.assertIn("Error", lines[1])
        self.assertIn("Warning", lines[2])
        self.assertEqual(len(lines), 3) # 3 lines, not 4
        
    def test_03_timer(self):
        """Test for class Timer.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("--------------------")
        print("Test for class Timer")
        print("--------------------")
        
        # Timer
        pathinfo = self.get_pathinfo()
        config = self.get_config(pathinfo)
        timerconfig = {}
        timerconfig['interval'] = config["window"]["interval"]
        timerconfig['times'] = config["database"]["times"]
        nightmode = config["window"]["nightmode"]
        timeframe = nightmode.get("timeframe")
        if timeframe is not None:
            timerconfig['nightmode_timeframe'] = timeframe
            ref = nightmode.get("colors")
            timerconfig['nightmode_colors'] = \
                config["window"]["colors"]["values"][ref]
        timer = Timer(timerconfig)

        # Interval
        hm = timer.get_timeset()['hm']
        interval = timer.get_interval()
        timeframe = interval['timeframe']
        secs1 = interval['seconds']
        secs2 = timerconfig['interval'].get(timeframe)
        print(f"Interval: {hm}, {timeframe}, {secs1}, {secs2}")
        self.assertEqual(secs1, secs2)

        # Times
        hm = timer.get_timeset()['hm']
        t1 = None
        t2 = None
        for t in timerconfig['times']:
            if t == hm:
                t1 = t
                break
        t2 = timer.timematch()
        print(f"Times: {hm}, {t1}, {t2}")
        if t1 is None:
            self.assertIsNone(t2)
        else:
            self.assertEqual(t1, t2)

        # Nightmode
        hm = timer.get_timeset()['hm']
        timeframe = timerconfig['nightmode_timeframe']
        nightmode_colors = timer.get_nightmode_colors()
        print(f"Nightmode: {hm}, {nightmode_colors}")
        if timer.is_intimeframe(timeframe, hm):
            self.assertIsNotNone(nightmode_colors)
        else:
            self.assertIsNone(nightmode_colors)

        # Timeshift
        t1 = "2024-02-28 23:59:00"
        t1a = "2024-02-29 00:00:00"
        t2 = "2024-02-29 23:59:00"
        t2a = "2024-03-01 00:00:00"
        secs = 60
        t = timer.timeshift(t1, secs)
        print(f"Timeshift: {t1}, {secs}, {t}")
        self.assertEqual(t, t1a)
        t = timer.timeshift(t2, secs)
        print(f"Timeshift: {t2}, {secs}, {t}")
        self.assertEqual(t, t2a)
        
        secs = -60
        t = timer.timeshift(t1a, secs)
        print(f"Timeshift: {t1a}, {secs}, {t}")
        self.assertEqual(t, t1)
        t = timer.timeshift(t2a, secs)
        print(f"Timeshift: {t2a}, {secs}, {t}")
        self.assertEqual(t, t2)

        # Timediff
        testsets = []
        testsets.append(['second', 60])
        testsets.append(['minute', 1.0])
        testsets.append(['hour', 0.0167])
        testsets.append(['day', 0.0007])
        for testset in testsets:
            unit = testset[0]
            diff1 = testset[1]
            diff2 = timer.timediff(t1, t1a, unit)
            print(f"Timediff: {t1}, {t1a}, {unit}, {diff2}")
            self.assertEqual(diff2, diff1)
            diff1 = testset[1] * -1
            diff2 = timer.timediff(t2a, t2, unit)
            print(f"Timediff: {t2a}, {t2}, {unit}, {diff2}")
            self.assertEqual(diff2, diff1)

        # Dateshift
        d1 = "2024-02-29"
        d2 = "2024-03-01"
        days = 1
        d = timer.dateshift(d1, days)
        print(f"Dateshift: {d1}, {days}, {d}")
        self.assertEqual(d, d2)
        days = -1
        d = timer.dateshift(d2, days)
        print(f"Dateshift: {d2}, {days}, {d}")
        self.assertEqual(d, d1)
        
    def test_04_fontscaler(self):
        """Test for class FontScaler.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("-------------------------")
        print("Test for class FontScaler")
        print("-------------------------")
                
        try:
            # FontScaler
            self.root = tk.Tk() # Required for fonts
            fontscaler = FontScaler()
            
            # Label font
            labelfont = fontscaler.get_labelfont()
            attr = labelfont.actual()
            print("Label font:")
            for entry in attr:
                print(f"{entry}: {attr.get(entry)}")
            self.assertIsNotNone(attr.get('family'))
            self.assertEqual(attr.get('weight'), "normal")
            
            # Value font
            valuefont = fontscaler.get_valuefont()
            attr = valuefont.actual()
            print("Value font:")
            for entry in attr:
                print(f"{entry}: {attr.get(entry)}")
            self.assertIsNotNone(attr.get('family'))
            self.assertEqual(attr.get('weight'), "normal")
                   
            # Value geometry
            valuegeometry = fontscaler.get_valuegeometry(240, 160)
            expected = (210, 130, 120, 87)
            print(f"Value geometry: {valuegeometry}")
            for i in range(len(valuegeometry)):
                print(f"{valuegeometry[i]}, {expected[i]}")
                self.assertEqual(valuegeometry[i], expected[i])
            
            # Value fontsize
            valuefontsize = fontscaler.get_valuefontsize(240, 160, "175")
            print(f"Value fontsize: {valuefontsize}")
            self.assertLess(valuefontsize, -1)

        finally:
            self.root.destroy()

    def test_05_device(self):
        """Test for device class Mock.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("----------------------------")
        print("Test for device class 'Mock'")
        print("----------------------------")
        
        # Mock
        pathinfo = self.get_pathinfo()
        config = self.get_config(pathinfo)
        device_config = config['devices']['Mock']
        device = Mock()
        device.set_config(device_config)
        
        # Infoset
        infoset = device.get_infoset()
        print("Device 'Mock' infoset:")
        for info in infoset:
            print(f"{info}: {infoset.get(info)}")
            self.assertEqual(type(infoset[info].get('power')), int)
            self.assertEqual(type(infoset[info].get('energy')), float)
            self.assertEqual(infoset[info].get('state'), 'ON')
            self.assertEqual(infoset[info].get('code'), 0)
            self.assertEqual(infoset[info].get('info'), '')
            self.assertEqual(infoset[info].get('trace'), '')
        
        # Close device
        device.close()

    def test_06_dbwriter_dbreader(self):
        """Test for classes DbWriter, DbReader.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("-----------------------------------")
        print("Test for classes DbWriter, DbReader")
        print("-----------------------------------")
        
        # DbWriter
        pathinfo = self.get_pathinfo()
        config = self.get_config(pathinfo)
        datapath = pathinfo['datapath']
        dbfile = f"{datapath}/db/monitor.db"
        if os.path.exists(dbfile):
            os.remove(dbfile)
        tablename = config['database']['tablename']
        columns = config['database']['columns']
        dbwriter = DbWriter(dbfile, tablename, columns)
        dbfile = dbwriter.get_dbfile()
        tabledef = dbwriter.get_tabledef()
        tablename = tabledef['tablename']
        print(f"Database file: '{dbfile}'")
        print(f"Table name: '{tablename}'")
        
        # DbWriter, DbReader
        dbreader = DbReader(dbfile)
        
        # Mock values
        columns = config['database']['columns']
        values = {}
        for column in columns:
            var = columns.get(column).get('var')
            val = int(1)
            if var == 'energy':
                val = float(1.5)
            value = {"code":0, var:val}
            units = columns.get(column).get('units')
            unitlist = units.split(',')
            for unit in unitlist:
                values[unit.strip()] = value
                
        # Write
        rowid = dbwriter.add_current_values(values)
        print(f"Row ID written: {rowid}")
        self.assertEqual(rowid, 1)
        
        # Read by ID
        columns, values = dbreader.select_by_id(tablename, rowid)
        print(f"Columns read: {columns}")
        print(f"Values read: {values}")
        self.assertEqual(columns[0], 'id')
        self.assertEqual(values[0], rowid)
        
        # Read by statement
        statement = f"select count(*) as rowcount from {tablename};"
        columns, values = dbreader.select_by_statement(statement)
        print(f"Columns read: {columns}")
        print(f"Values read: {values}")
        self.assertEqual(columns[0], 'rowcount')
        self.assertEqual(values[0][0], 1)

    def test_07_requester_responder(self):
        """Test for classes Requester, Responder.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("-------------------------------------")
        print("Test for classes Requester, Responder")
        print("-------------------------------------")

        # Requester, responder
        pathinfo = self.get_pathinfo()
        config = self.get_config(pathinfo)
        port = 42002 # overwrite config
        logger = self.get_logger()
        try:
            
            # Responder thread
            tasktrigger = Queue()
            responder = Responder(port, tasktrigger, logger)
            thread = Thread(target=responder.listen, args=())
            thread.daemon = True
            thread.start()
            
            # Requester thread
            data = Queue()
            thread = Thread(target=self.request, args=(port, logger, data))
            thread.daemon = True
            thread.start()
            
            # Wait for task from responder, set response data
            task = tasktrigger.get()
            response = {"test_response":"Hello"}
            responder.set_data(response)
            tasktrigger.task_done()

            # Response received
            response_received = data.get()
            print(f"Response sent    : {response}")
            print(f"Response received: {response_received}")
            self.assertEqual(str(response), str(response_received))

        finally:
            if responder:
               responder.close()
               print(f"Responder closed.")

    def test_08_monitor(self):
        """Test for class Monitor.
        
        This class requires a user test.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("----------------------")
        print("Test for class Monitor")
        print("----------------------")
        
        print("This class requires a user test.")

    def test_09_window(self):
        """Test for class Window.
        
        This class requires a user test.

        Args:
           None.

        Returns:
           None.
        """
        print("\n")
        print("---------------------")
        print("Test for class Window")
        print("---------------------")
        
        print("This class requires a user test.")

    # ------------------        
    # Additional methods
    # ------------------
    
    def get_pathinfo(self):
        """Gets the application path information.

        Args:
           None.

        Returns:
           dict: The application path information.
        """
        return PathFinder().get_pathinfo(TEST_DATAPATH)
        
    def get_config(self, pathinfo:dict):
        """Gets the test configuration.

        Args:
           pathinfo (dict): The application path information.

        Returns:
           dict: The test configuration.
        """
        configfile = pathinfo.get('configfile')
        with open(configfile, 'r') as f:
            config = json.load(f)
        return config
        
    def get_logger(self):
        """Gets a logger instance.

        Args:
           None.

        Returns:
           object: The logger instance.
        """
        # Get pathinfo and config
        pathinfo = self.get_pathinfo()
        config = self.get_config(pathinfo)
                
        # Remove apptest logfiles
        logdir = f"{pathinfo['datapath']}/log"
        self.remove_logfiles(logdir, 'apptest')
        
        # Set and return logger
        loggerconfig = {}
        loggerconfig['datapath'] = pathinfo['datapath']
        loggerconfig['loglevel'] = 'info'       # overwrite config
        loggerconfig['logtofile'] = 'true'      # overwrite config
        loggerconfig['logsource'] = 'apptest'   # overwrite config
        return Logger(loggerconfig)
        
    def get_loglines(self, logfile):
        """Gets the valid loglines from the given logfile.
        
        Valid loglines consist of date, time, code, and text.

        Args:
           logfile (str): Absolute path to the logfile.

        Returns:
           list: The loglines read.
        """
        loglines = []
        with open(logfile, "r") as f:
            for line in f:
                logline = line.rstrip()
                parts = logline.split(' ')
                if len(parts) >= 4:
                    loglines.append(logline)
        return loglines
        
    def remove_logfiles(self, logdir, logsource):
        """Gets the loglines from the given logfile.

        Args:
           logdir (str): The logfile directory.
           logsource (str): The log source, e.g. 'monitor'.

        Returns:
           None.
        """
        for name in os.listdir(logdir):
            if name.endswith(".log") and name.startswith(logsource):
                logfile = f"{logdir}/{name}"
                os.remove(logfile)
                print(f"Logfile removed: '{logfile}'")
 
    def request(self, port:int, logger:object, data:object):
        """Triggers a request.

        Args:
            port (int): The responder port.
            logger (object): Logger instance.
            data (str): Response data queue.

        Returns:
           None.
        """
        requester = Requester(port, logger)
        data.put(requester.request())
        requester.close()
        print(f"Rquester closed.")

# ----
# Main
# ----

if __name__ == '__main__':
    unittest.main()
