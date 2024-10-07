# -*- coding: utf-8 -*-
"""mywattsmon"""

import random
import traceback

class Mock:

    """
    This class 'mocks' a real device class for testing.

    For more information see documentation.
    """

    def __init__(self):
        """Class setup.
        
        Args:
            None

        Returns:
            None.
        """
        self.config = None

    def set_config(self, config:dict):
        """Sets the configuration for this device.

        Args:
            config (dict): Specifications from the configuration file.

        Returns:
            None.
        """
        self.config = config
        self.units = config['units']
        
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
        num = 0
        for unit in self.units:
            num += 1
            uid = self.units[unit]['uid']
            infoset[unit] = self.__get_info(uid, num)
        return infoset
    
    # ---------------
    # Private methods
    # ---------------

    def __get_info(self, uid:str, num:int):
        """Gets information from a specific device unit.

        Args:
            uid (str): Unit ID.
            num (int): A number.

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
            result = self.__get_data(num)
            data['power'] = int(result['power'])
            data['energy'] = round(float(result['energy']), 1)
            data['state'] = 'ON'
            data['code'] = 0
        except:
            data['code'] = 1
            data['info'] = 'Error'
            data['trace'] = self.__get_trace()
        return data

    def __get_data(self, num:int):
        """Gets data from the device.

        Args:
            num (int): A number.
    
        Returns:
            dict: Power and energy.
        """
        data = {}
        power = int(num + 10)
        if num == 1:
            power += random.randint(-50, 50)
        else:
            power += random.randint(0, 250)
        energy = round(float((num * 12) + 1115.5) + random.random(), 1)
        data["power"] = power
        data["energy"] = energy
        return data
        
    def __get_trace(self):
        """Gets a limited traceback output in a single line.

        Args:
            None.
    
        Returns:
            str: The traceback line.
        """
        tb = traceback.format_exc(limit=1,chain=False)
        return ' '.join(str(tb).split())
