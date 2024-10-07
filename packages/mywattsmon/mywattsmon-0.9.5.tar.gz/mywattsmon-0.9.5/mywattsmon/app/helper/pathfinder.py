# -*- coding: utf-8 -*-
"""mywattsmon"""

import glob
import os
import shutil

from mywattsmon.app.helper.configwriter import ConfigWriter

ROOTDIR = "/mywattsmon"
SUBDIRS = ["/app", "/app/device", "/app/helper", "/doc", "/test"]
USERDIR = "/app/device/user"
CONFIGFILE = "/config.json"

class PathFinder:
    
    """
    PathFinder class.
    """

    def __init__(self):
        """Setup - here only formally.

        Args:
            None.

        Returns:
            None.
        """
        pass
        
    def get_pathinfo(self, datapath:str=None):
        """Gets the application path information.
        
        Also creates not existing paths and configuration file.
         
        Args:
           datapath (str): The application's data path, or None.

        Returns:
           dict: Application path information.
        """
        pathinfo = {}
        apphome = None
        path = os.path.dirname(os.path.abspath(__file__))
        path = path.replace('\\', '/')
        if not os.path.exists(f"{path}{ROOTDIR}"):
            for subdir in SUBDIRS:
                if path.endswith(subdir):
                    pos = path.rfind(subdir)
                    apphome = path[:pos]
                    break
        if apphome is None or not os.path.exists(apphome):
            return None
        for subdir in SUBDIRS:
            if not os.path.exists(f"{apphome}{subdir}"):
                return None
                
        # apphome
        pathinfo['apphome'] = apphome
        
        # datapath
        path = None
        if datapath is None:
            path = f"{apphome}-data"
        else:
            path = datapath
        absdatapath = os.path.abspath(path)
        absdatapath = absdatapath.replace('\\', '/')
        if not os.path.exists(absdatapath):
            os.makedirs(absdatapath)
        pathinfo['datapath'] = absdatapath
        dbpath = f"{absdatapath}/db"
        logpath = f"{absdatapath}/log"
        pypath = f"{absdatapath}/py"
        if not os.path.exists(dbpath):
            os.makedirs(dbpath)
        if not os.path.exists(logpath):
            os.makedirs(logpath)
        if not os.path.exists(pypath):
            os.makedirs(pypath)
        
        # userdir
        for p in glob.glob(f"{pypath}/*.py", recursive=False):
            if os.path.isfile(p):
                shutil.copy2(p, f"{apphome}{USERDIR}")
        
        # configfile
        pathinfo['configfile'] = f"{absdatapath}{CONFIGFILE}"
        if not os.path.exists(pathinfo['configfile']):
            ConfigWriter().write_configfile(pathinfo['configfile'])

        return pathinfo
