# -*- coding: utf-8 -*-
"""mywattsmon"""

import traceback
import minimalmodbus

MODE = minimalmodbus.MODE_RTU
PARITY = minimalmodbus.serial.PARITY_NONE
BYTEORDER = minimalmodbus.BYTEORDER_BIG
BAUDRATE = 9600
BYTESIZE = 8
STOPBITS = 1
TIMEOUT = 3

class DTSU:

    """
    This device class communicates via Modbus RTU with a Chint energy
    meter named 'DTSU666' that operates as Modbus slave.

    Requires: pip install minimalmodbus

    This class wraps the following minimalmodbus/DTSU requests:
        
        - read_float(4137, ...) -> kWh total
        - read_float(8211, ...) -> W current
    
    It is assumed that the energy meter is connected to a serial port
    via USB adapter. On Linux, the serial port is specified as follows:
    /dev/ttyUSB<n>, e.g. /dev/ttyUSB0. On Windows: COM<n>, e.g. COM3.

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
        for unit in self.units:
            port = self.units[unit]['port']
            address = self.units[unit]['address']
            infoset[unit] = self.__get_info(port, address)
        return infoset

    # ---------------
    # Private methods
    # ---------------

    def __get_info(self, port:str, address:int):
        """Gets information from a specific device unit.

        Args:
            port (str): Serial port, e.g. /dev/ttyUSB1).
            address (int): Modbus address, e.g. 68).

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
            result = self.__get_data(port, address)
            data['power'] = int(result['power'])
            data['energy'] = round(float(result['energy']), 1)
            data['state'] = 'ON'
            data['code'] = 0
        except:
            data['code'] = 1
            data['info'] = 'Error'
            data['trace'] = self.__get_trace()
        return data

    def __get_data(self, port:str, address:int):
        """Gets data from the device.

        Args:
            port (str): Serial port, e.g. /dev/ttyUSB1).
            address (int): Modbus address, e.g. 68).
    
        Returns:
            dict: Power and energy.
        """
        data = {}
        try:
            # --------------
            # Setup instance
            # --------------
            dtsu = minimalmodbus.Instrument(port, address)
            dtsu.serial.mode = MODE
            dtsu.serial.baudrate = BAUDRATE
            dtsu.serial.parity = PARITY
            dtsu.serial.stopbits = STOPBITS
            dtsu.serial.bytesize = BYTESIZE
            dtsu.serial.timeout = TIMEOUT
            dtsu.clear_buffers_before_each_transaction = True
            dtsu.close_port_after_each_call = True
            # ------------
            # Receive data
            # ------------
            data["power"] = round((
                dtsu.read_float(8211, 4, 2, BYTEORDER) * 0.1), 4
                )
            data["energy"] = round(abs(
                dtsu.read_float(4137, 4, 2, BYTEORDER)), 4
                )
            return data
        finally:
            if dtsu:
                dtsu.serial.close()
                
    def __get_trace(self):
        """Gets a limited traceback output in a single line.

        Args:
            None.
    
        Returns:
            str: The traceback line.
        """
        tb = traceback.format_exc(limit=1,chain=False)
        return ' '.join(str(tb).split())

