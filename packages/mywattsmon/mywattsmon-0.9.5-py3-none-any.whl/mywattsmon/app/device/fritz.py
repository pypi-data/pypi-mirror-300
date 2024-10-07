# -*- coding: utf-8 -*-
"""mywattsmon"""

import traceback
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

PORT = 49000

class Fritz:

    """
    This device class communicates with a FRITZ!Box via HTTP respectively
    TR-064.

    Requires: pip install fritzconnection

    Assuming that communication takes place exclusively in the local
    network, only HTTP, not HTTPS, is supported here.

    For more information see documentation.
    """

    def __init__(self):
        """Class 'Fritz' setup.
        
        Args:
            None.

        Returns:
            None.
        """
        self.config = None
        self.units = None
        self.fritz = None
    
    def set_config(self, config:dict):
        """Sets the configuration for this device.

        Args:
            config (dict): Specifications from the configuration file.

        Returns:
            None.
        """
        self.config = config
        self.units = config['units']
        self.fritz = FritzHomeAutomation(
            address=config['connection']['address'],
            port=PORT,
            user=config['connection']['user'],
            password=config['connection']['password'],
            use_tls=False)
            
    def close(self):
        """Close resources as needed.

        Args:
            None.

        Returns:
            None.
        """
        pass # Nothing to close here, but formally required.

    def get_infoset(self):
        """Gets information from all configured device units.
        
        The form of the result is standardized. See the comment
        on this method in the base class.

        Args:
            None.

        Returns:
            dict: The data of all units as infoset.
        """
        infoset = {}
        for unit in self.units:
            uid = self.units[unit]['uid']
            infoset[unit] = self.__get_info(uid)
        return infoset

    def set_switch(self, uid:str, state:str):
        """Switches a Fritz plug device on or off.

        Args:
            uid (str): Unit ID, e.g. 11630 043....
            state (str): ON or OFF.
    
        Returns:
           None.
        """
        if state == 'ON':
            self.fritz.set_switch(uid, on=True)
        elif state == 'OFF':
            self.fritz.set_switch(uid, on=False)
        else:
            pass

    # ---------------
    # Private methods
    # ---------------

    def __get_info(self, uid:str):
        """Gets information from a Fritz device.

        Args:
            uid (str): Unit ID.

        Returns:
            dict: The information as key value pairs.
        """
        data = {}
        data['power'] = None
        data['energy'] = None
        data['state'] = 'OFF'
        data['code'] = 2
        data['info'] = ''
        data['trace'] = ''
        try: 
            result = self.__get_data(uid)
            if result is not None:
                data['power'] = int(result['NewMultimeterPower'] / 100)
                data['energy'] = \
                    round(float(result['NewMultimeterEnergy'] / 1000), 1)
                data['state'] = result['NewSwitchState']
                tempc = \
                    round(float(result['NewTemperatureCelsius'] / 10), 1)
                data['info'] = f'tempc={tempc}'
                data['code'] = 0
        except:
            data['code'] = 1
            data['info'] = 'Error'
            data['trace'] = self.__get_trace()
        return data

    def __get_data(self, uid:str):
        """Gets data from a Fritz device unit via Fritz hub.

        Args:
            uid (str): Unit ID, e.g. 11630 043....
    
        Returns:
            dict: The result data.
        """
        return self.fritz.get_device_information_by_identifier(uid)

    def __get_overall_data(self):
        """Gets overall device data from a Fritz hub.
             
        Args:
            None.
    
        Returns:
           list of dict: The result data n times.
        """
        return self.fritz.device_information()
        
    def __get_trace(self):
        """Gets a limited traceback output in a single line.

        Args:
            None.
    
        Returns:
            str: The traceback line.
        """
        tb = traceback.format_exc(limit=1,chain=False)
        return ' '.join(str(tb).split())

