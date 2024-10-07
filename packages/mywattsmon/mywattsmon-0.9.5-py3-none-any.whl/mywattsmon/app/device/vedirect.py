# -*- coding: utf-8 -*-
"""mywattsmon"""

import serial
import traceback

BAUDRATE = 19200
BYTESIZE = 8
PARITY = 'N'
STOPBITS = 1
TIMEOUT = 3
EXPECTED_KEYS = ['FW', 'SER#', 'V', 'I', 'VPV', 'PPV', 'CS', 'MPPT',
    'OR', 'ERR', 'LOAD', 'IL', 'H19', 'H20', 'H21', 'H22', 'H23',
    'HSDS', 'PID']
MAX_ENTRIES = 24

class VEDirect:

    """
    This device class reads VE-Direct communication parameters from a
    Victron Energy SmartSolar charger device, e.g. MPPT 75|10.

    It is assumed that the VE device is connected to a serial port
    via USB adapter. On Linux, the serial port is specified as follows:
    /dev/ttyUSB<n>, e.g. /dev/ttyUSB1. On Windows: COM<n>, e.g. COM3.
     
    Requires: An original VE-Direct USB to UART cable.
    
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
            infoset[unit] = self.__get_info(port)
        return infoset

    # ---------------
    # Private methods
    # ---------------

    def __get_info(self, port:str):
        """Gets information from a VE device.

        Args:
            port (str): Serial port, e.g. /dev/ttyUSB0.
    
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
            result = self.__get_data(port)
            if result is not None:
                errors = []
                power = result.get('PPV')
                energy = result.get('H19')
                cs = result.get('CS')
                if power is not None and type(power) is not str:
                    data['power'] = int(power)
                else:
                    errors.append(f"power={power}")
                if energy is not None and type(energy) is not str:
                    data['energy'] = round(float(energy), 1)
                else:
                    errors.append(f"energy={energy}")
                if cs is not None and type(cs) is not str:
                    if cs > 0:
                        data['state'] = 'ON'
                else:
                    errors.append(f"cs={cs}")
                if len(errors) > 0:
                    data['info'] = 'Error'
                    data['trace'] = ' '.join(errors)
                    data['code'] = 1
                else:
                    data['info'] = f"cs={cs}"
                    data['trace'] = ''
                    data['code'] = 0
        except:
            data['code'] = 1
            data['info'] = 'Error'
            data['trace'] = self.__get_trace()
        return data

    def __get_data(self, port:str):
        """Gets data from device.

        Args:
            port (str): Serial port, e.g. /dev/ttyUSB0.
    
        Returns:
            dict: The complete parsed result data.
        """
        data = {}
        count = 0
        key_count = 0
        with serial.Serial(port=port, baudrate=BAUDRATE,
            bytesize=BYTESIZE, parity=PARITY, stopbits=STOPBITS,
            timeout=TIMEOUT) as conn:
            while True:
                b = conn.readline()
                if b == b'':
                    return None # No result after timeout
                count += 1
                if str(b).find('\\t') > 0:
                    try:
                        key, value = b.decode('utf-8').split('\t')
                    except:
                        continue
                    if key in EXPECTED_KEYS:
                        key_count += 1
                        data[key] = str(value)
                if key_count == len(EXPECTED_KEYS):
                    return self.__parse_data(data)
                if count > MAX_ENTRIES:
                    return None # Invalid result

    def __parse_data(self, data:dict):
        """Parses data from the VE device.

        Args:
            data (dict): Result data.
    
        Returns:
            dict: The parsed result data.
        """
        result = {}
        for key in EXPECTED_KEYS:
            value = data.get(key)
            if value is None:
                result[key] = None
                continue
            try:
                value = str(value).strip()
                if key in ('V', 'I', 'VPV', 'IL'):
                    value = float(value) / 1000
                elif key in ('H19', 'H20', 'H22'):
                    value = float(value) * 0.01
                elif key in ('PPV', 'CS', 'MPPT', 'ERR', 'H21',
                             'H23', 'HSDS'):
                    value = int(value)
                else:
                    pass
            except:
                value = None
            result[key] = value
        return result
        
    def __get_trace(self):
        """Gets a limited traceback output in a single line.

        Args:
            None.
    
        Returns:
            str: The traceback line.
        """
        tb = traceback.format_exc(limit=1,chain=False)
        return ' '.join(str(tb).split())
