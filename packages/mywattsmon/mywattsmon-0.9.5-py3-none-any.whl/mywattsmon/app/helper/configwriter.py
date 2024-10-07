# -*- coding: utf-8 -*-
"""mywattsmon"""

import os

class ConfigWriter:
    
    """
    ConfigWriter class.
    """

    def __init__(self):
        """Setup - here only formally.

        Args:
            None.

        Returns:
            None.
        """
        pass
        
    def write_configfile(self, configfile:str):
        """Writes a configuration file from internal content.

        Args:
           configfile (str): Absolute path to the configfile, named
                             'config.json' or 'test_config.json'.

        Returns:
           bool. True if the file was written, else False.
        """
        if configfile.endswith('config.json'):
            lines = self.get_content().splitlines(keepends=True)
        else:
            return False
        with open(configfile, 'w') as f:
            for line in lines:
                f.write(line)
        return True

    def get_content(self):
        """Gets the (default) configuration file content.
        
        Args:
           None.

        Returns:
           str: The content.
        """
        return \
        '{\n'\
        '    "title":"mywattsmon configuration",\n'\
        '    "loglevel":"info",\n'\
        '    "logtofile":"false",\n'\
        '    "port":"42001",\n'\
        '    "window":{\n'\
        '        "title":"Status",\n'\
        '        "size":"max",\n'\
        '        "interval":{"default":30,"20:00-22:00":60,"22:00-05:00":300},\n'\
        '        "nightmode":{"timeframe":"22:00-05:00","colors":"ref0"},\n'\
        '        "colors":{\n'\
        '            "window":{"bg":"gray7"},\n'\
        '            "values":{\n'\
        '                "ref0":{"bg":"black","fg":"gray7"},\n'\
        '                "ref1":{\n'\
        '                    "bg+":"darkseagreen","fg+":"white",\n'\
        '                    "bg-":"#FFCFC9","fg-":"black"\n'\
        '                },\n'\
        '                "ref2":{"bg":"#FFCFC9","fg":"black"},\n'\
        '                "ref3":{"bg":"steelblue4","fg":"white"},\n'\
        '                "ref4":{"bg":"khaki","fg":"black"},\n'\
        '                "ref5":{"bg":"darkolivegreen1","fg":"black"},\n'\
        '                "ref6":{"bg":"gray7","fg":"white"}\n'\
        '            }\n'\
        '        },\n'\
        '        "grid":{\n'\
        '            "W":{\n'\
        '                "units":"M1","var":"power","colors":"ref1",\n'\
        '                "rownum":0,"colnum":0,"rowspan":2,"colspan":2\n'\
        '            },\n'\
        '            "kWh":{\n'\
        '                "units":"M1","var":"energy","colors":"ref2",\n'\
        '                "rownum":0,"colnum":2,"rowspan":2,"colspan":3\n'\
        '            },\n'\
        '            "L1":{\n'\
        '                "units":"M2,M3","var":"power","colors":"ref3",\n'\
        '                "rownum":2,"colnum":0,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "L2":{\n'\
        '                "units":"M4","var":"power","colors":"ref3",\n'\
        '                "rownum":2,"colnum":1,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "L3":{\n'\
        '                "units":"M5","var":"power","colors":"ref3",\n'\
        '                "rownum":2,"colnum":2,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "L4":{\n'\
        '                "units":"M6,M7,M8,M9","var":"power","colors":"ref3",\n'\
        '                "rownum":2,"colnum":3,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "CHARGE":{\n'\
        '                "units":"M10","var":"power","colors":"ref3",\n'\
        '                "rownum":2,"colnum":4,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "FEED1":{\n'\
        '                "units":"M11","var":"power","colors":"ref4",\n'\
        '                "rownum":3,"colnum":0,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "FEED2":{\n'\
        '                "units":"M12","var":"power","colors":"ref4",\n'\
        '                "rownum":3,"colnum":1,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "BATT1":{\n'\
        '                "units":"M13","var":"power","colors":"ref5",\n'\
        '                "rownum":3,"colnum":2,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "BATT2":{\n'\
        '                "units":"M14","var":"power","colors":"ref5",\n'\
        '                "rownum":3,"colnum":3,"rowspan":1,"colspan":1\n'\
        '            },\n'\
        '            "Refresh":{\n'\
        '                "units":"<refresh>","var":"<countdown>","colors":"ref6",\n'\
        '                "rownum":3,"colnum":4,"rowspan":1,"colspan":1\n'\
        '            }\n'\
        '        }\n'\
        '    },\n'\
        '    "database":{\n'\
        '        "times":["00:00","03:00","06:00","09:00","12:00","15:00",\n'\
        '                "18:00","21:00","23:59"],\n'\
        '        "tablename":"kwh",\n'\
        '        "columns":{\n'\
        '            "em":{"units":"M1","var":"energy"},\n'\
        '            "l1":{"units":"M2,M3","var":"energy"},\n'\
        '            "l2":{"units":"M4","var":"energy"},\n'\
        '            "l3":{"units":"M5","var":"energy"},\n'\
        '            "l4":{"units":"M6,M7,M8,M9","var":"energy"},\n'\
        '            "charge":{"units":"M10","var":"energy"},\n'\
        '            "feed1":{"units":"M11","var":"energy"},\n'\
        '            "feed2":{"units":"M12","var":"energy"},\n'\
        '            "batt1":{"units":"M13","var":"energy"},\n'\
        '            "batt2":{"units":"M14","var":"energy"}\n'\
        '        }\n'\
        '    },\n'\
        '    "devices":{\n'\
        '        "Mock":{\n'\
        '            "module":"mywattsmon.app.device.mock",\n'\
        '            "units":{\n'\
        '                "M1":{"uid":"m1"},\n'\
        '                "M2":{"uid":"m2"},\n'\
        '                "M3":{"uid":"m3"},\n'\
        '                "M4":{"uid":"m4"},\n'\
        '                "M5":{"uid":"m5"},\n'\
        '                "M6":{"uid":"m6"},\n'\
        '                "M7":{"uid":"m7"},\n'\
        '                "M8":{"uid":"m8"},\n'\
        '                "M9":{"uid":"m9"},\n'\
        '                "M10":{"uid":"m10"},\n'\
        '                "M11":{"uid":"m11"},\n'\
        '                "M12":{"uid":"m12"},\n'\
        '                "M13":{"uid":"m13"},\n'\
        '                "M14":{"uid":"m14"}\n'\
        '            }\n'\
        '        }\n'\
        '    }\n'\
        '}\n'
