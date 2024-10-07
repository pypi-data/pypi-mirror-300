# -*- coding: utf-8 -*-
"""mywattsmon"""

import json
import requests
import traceback

PORT = 8444
TIMEOUT = 5 # Seconds
HEADERS = {"content-type": "application/json", "api-version": "3.3"}
GET_SERVICES_AS_ARRAY = f"https://--address-:{PORT}/smarthome/services"
PUT_POWER_SWITCH = f"https://--address-:{PORT}/smarthome/devices/--uid-" \
                   f"/services/PowerSwitch/state"
PUT_POWER_SWITCH_ON = {'@type': "powerSwitchState", 'switchState': "ON"}
PUT_POWER_SWITCH_OFF = {'@type': "powerSwitchState", 'switchState': "OFF"}

class Bosch:

    """
    This device class communicates with a BOSCH Smart Home Controller II
    (SHC II) via HTTPS.

    Requires: pip install requests

    A session is not opened to preserve the statelessness typical of
    REST services.

    Before this class can be used, an API client must be registered at
    BOSCH SHC II, and, due to the mandatory HTTPS, certificate files
    must be created.

    For more information see documentation.
    """

    def __init__(self):
        """Class setup.

        Args:
            None.

        Returns:
            None.
        """
        self.config = None
        self.units = None
        self.address = None
        self.certfile = None
        self.keyfile = None
        self.cacertfile = None
        # ----------------------------------------------------------
        # CA/Server verification is optional here due to complex and
        # error-prone handling of CA certificate chain, server name,
        # etc. If no path to CA certificate is configured, urllib3
        # warnings might be disabled to avoid InsecureRequestWarning
        # ----------------------------------------------------------
        try:
            from urllib3 import disable_warnings
            disable_warnings()
        except:
            pass # Ignore exception in this case

    def set_config(self, config:dict):
        """Sets the configuration for this device.

        Args:
            config (dict): Specifications from the configuration file.

        Returns:
            None.
        """
        self.config = config
        self.units = config['units']
        self.address = config['connection']['address']
        self.certfile = config['connection']['certfile']
        self.keyfile = config['connection']['keyfile']
        
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
        try:
            overall_info = self.__get_overall_info()
            for unit in self.units:
                uid = self.units[unit]['uid']
                infoset[unit] = self.__get_info(uid, overall_info)
        except:
            trace = self.__get_trace()
            for unit in self.units:
                uid = self.units[unit]['uid']
                infoset[unit] = self.__get_error_info(uid, trace)
        return infoset

    def set_switch(self, uid:str, state:str):
        """Switches a Bosch plug unit on or off.

        Args:
            uid (str): Unit ID, e.g. hdm:ZigBee:70ac08fffefd....
            state (str): ON or OFF.
    
        Returns:
           Response: The response.
        """
        data = None
        if state == "ON":
            data = PUT_POWER_SWITCH_ON
        elif state == "OFF":
            data = PUT_POWER_SWITCH_OFF
        else:
            pass
        url = PUT_POWER_SWITCH.replace("--address-", self.address)
        url = url.replace("--uid-", uid)
        return self.__PUT(url, data)

    # ---------------
    # Private methods
    # ---------------
    
    def __get_overall_info(self):
        """Gets information over all Bosch device units.

        None.
    
        Returns:
            dict: The result data.
        """
        return self.__get_overall_data()

    def __get_info(self, uid:str, overall_info:dict):
        """Gets information from a specific device unit.
        
        For this device, data is received from the given result,
        collected before via get_overall_info.

        Args:
            uid (str): Unit ID.
            overall_info (str): Result from get_overall_info.

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
            result = None
            for entity_id in overall_info:
                if entity_id == uid:
                    result = overall_info.get(uid)
                    break;
            if result is not None:
                data['power'] = int(result['power'])
                data['energy'] = round(float(result['energy'] / 1000), 1)
                data['state'] = result['state']
                data['code'] = 0
        except:
            data['code'] = 1
            data['info'] = 'Error'
            data['trace'] = self.__get_trace()
        return data
        
    def __get_error_info(self, uid:str, trace:str):
        """Gets error information for a specific device unit.
 
         Args:
            uid (str): Unit ID.
            trace (str): Exception trace.

        Returns:
            dict: The error information as key value pairs.
        """
        data = {}
        data['power'] = None
        data['energy'] = None
        data['state'] = 'OFF'
        data['code'] = 1
        data['info'] = 'Error'
        data['trace'] = trace
        return data

    def __get_overall_data(self):
        """Gets overall data from Bosch device units.

        Args:
            None.
    
        Returns:
            dict: The result data.
        """
        # -------------------------------------------------------
        # Get overall data, then specific data from the response.
        # This is much faster than explicit device requests.
        # -------------------------------------------------------
        url = GET_SERVICES_AS_ARRAY.replace("--address-", self.address)
        response = self.__GET(url)
        data = json.loads(response.text)
        power = None
        energy = None
        state = None
        result = {}
        for entity in data:
            data = {}
            entity_devid = entity.get("deviceId")
            value = entity.get("id")
            if value is not None:
                if value == "PowerMeter":
                    power = entity['state']['powerConsumption']
                    energy = entity['state']['energyConsumption']
                elif value == "PowerSwitch":
                    state = entity['state']['switchState']
                else:
                    continue
            data["state"] = state
            data["power"] = power
            data["energy"] = energy
            result[entity_devid] = data
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

    def __GET(self, url:str):
        """Performs a GET request against a REST API.
        
        Args:
            url (str): The URL string.

        Returns:
            Response: The response.
        """
        # --------------------------------------------------------------
        # CA/Server verification optional due to complex and error-prone
        # handling of CA certificate chain, server name, etc:
        # --------------------------------------------------------------
        verify_option = False
        if self.cacertfile is not None:
            verify_option = self.cacertfile
        # -------
        # Request
        # -------
        response = requests.get(url,
                                headers = HEADERS,
                                timeout = TIMEOUT,
                                cert = (self.certfile,
                                        self.keyfile),
                                verify = verify_option
                                )
        response.raise_for_status()
        return response

    def __PUT(self, url:str, data:dict):
        """Performs a PUT request against a REST API.

        Args:
            url (str): The URL string.
            data (dict): The PUT data.

        Returns:
            Response: The response.
        """
        # --------------------------------------------------------------
        # CA/Server verification optional due to complex and error-prone
        # handling of CA certificate chain, server name, etc:
        # --------------------------------------------------------------
        verify_option = False
        if self.cacertfile is not None:
            verify_option = self.cacertfile
        # -------
        # Request
        # -------
        response = requests.put(url,
                                headers = HEADERS,
                                json = data,
                                timeout = TIMEOUT,
                                cert = (self.certfile,
                                        self.keyfile),
                                verify = verify_option
                                )
        response.raise_for_status()
        return response
