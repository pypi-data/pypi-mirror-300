# -*- coding: utf-8 -*-
"""mywattsmon"""

class Abstract:

    """
    This class is an informal Python interface and acts as a blueprint
    for all device classes. Each device class implements (overrides)
    its abstract methods.
    """

    def set_config(self, config:dict):
        """Sets the configuration for this device as needed.

        Args:
            config (dict): Specifications from the configuration file.

        Returns:
            None.
        """
        pass
        
    def close(self):
        """Closes resources as needed.

        Args:
            None.

        Returns:
            None.
        """
        pass

    def get_infoset(self):
        """Gets information from all configured device units.
        
        The form of the result is standardized. The following data
        must be supplied for each unit:
        
        data = {}
        data['power'] = 0
        data['energy'] = 0.0
        data['state'] = 'OFF'
        data['code'] = 2
        data['info'] = ''
        data['trace'] = ''
        
        infoset = {}
        infoset[<unit1>] = <data_from_unit1>
        infoset[<unit2>] = <data_from_unit2>
        infoset[<unit3>] = <data_from_unit3>
        ...
        
        See also the code of the implemented device classes.

        Args:
            None.

        Returns:
            dict: The data of all units as 'infoset'.
        """
        pass
