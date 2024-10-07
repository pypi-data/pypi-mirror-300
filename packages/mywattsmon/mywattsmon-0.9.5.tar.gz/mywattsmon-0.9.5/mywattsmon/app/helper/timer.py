# -*- coding: utf-8 -*-
"""mywattsmon"""

import time
import datetime

class Timer:

    """
    Timer class.
    """

    def __init__(self, config:dict):
        """Setup.

        Args:
            config (dict): Specific timer configuration.

        Returns:
            None.
        """
        self.interval = config.get('interval')
        self.times = config.get('times')
        self.nightmode_timeframe = config.get('nightmode_timeframe')
        self.nightmode_colors = config.get('nightmode_colors')
                
    def get_interval(self):
        """Gets current interval information.
         
        Args:
           None.

        Returns:
           dict: The current interval information.
        """
        # Set default interval and timeframe
        seconds = int(self.interval['default'])
        timeframe = "default"

        # Set current time with various segments
        timeset = self.get_timeset()
        
        # Find the current timeframe as configured
        for item in self.interval:
            if item == 'default':
                continue
            if self.is_intimeframe(item, timeset['hm']):
                seconds = int(self.interval[item])
                timeframe = item
                break

        # Set nexttime
        nexttime = self.timeshift(timeset.get('dhms'), seconds)
        
        # Set and return info
        info = {}
        info['timeset'] = timeset
        info['seconds'] = seconds
        info['timeframe'] = timeframe
        info['nexttime'] = nexttime[11:]
        return info
        
    def timematch(self):
        """Checks whether the current time matches a configured time.
         
        Args:
           None.

        Returns:
           str: Time if the current time matches, else None.
        """
        t1 = self.get_timeset()['hm']
        for t2 in self.times:
            if t1 == t2:
                return t1
        return None
        
    def get_nightmode_colors(self):
        """Gets nighmode colors within a nightmode timeframe.
         
        Args:
           None.

        Returns:
           dict: Nightmode colors if the condition is met, else None.
        """
        if self.nightmode_timeframe is None:
            return None
        timeset = self.get_timeset()
        if self.is_intimeframe(
            self.nightmode_timeframe, timeset['hm']
            ):
            return self.nightmode_colors
        return None
 
    def get_timeset(self):
        """Gets the current time in various segments.
         
        Args:
           None.

        Returns:
           int: The current time in various segments.
        """
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        timeset = {}
        timeset["dhms"] = ts         # %Y-%m-%d %H:%M:%S"
        timeset['dhm'] = ts[:16]     # %Y-%m-%d %H:%M
        timeset['dh'] = ts[:13]      # %Y-%m-%d %H
        timeset['d'] = ts[:10]       # %Y-%m-%d
        timeset['hms'] = ts[11:]     # %H:%M:%S
        timeset['hm'] = ts[11:-3]    # %H:%M
        timeset['h'] = ts[11:-6]     # %H
        timeset['m'] = ts[14:-3]     # %M
        timeset['s'] = ts[17:]       # %S
        return timeset
        
    def is_intimeframe(self, timeframe_hm:str, time_hm:str):
        """Checks if the given time is within the given timeframe
         
        Args:
           timeframe_hm (str): Timeframe formatted %H:%M-%H:%M
           time_hm (str): Time formatted %H:%M

        Returns:
           bool: True if the condition is met, else False.
        """
        hm_a, hm_b = timeframe_hm.split("-")
        hm1 = int(f"1{hm_a.replace(':', '')}")
        hm2 = int(f"1{hm_b.replace(':', '')}")
        hm3 = int(f"1{time_hm.replace(':', '')}")
        met = False
        if hm1 > hm2:
            # e.g. 17:00-05:00, 06:30-04:00 23:00-22:00
            if hm3 >= hm1 or hm3 <= hm2:
                met = True
        else:
            # e.g. 17:00-18:00, 04:00-23:00
            if hm3 >= hm1 and hm3 <= hm2:
                met = True
        return met
         
    def timeshift(self, timestamp:str, shift:int):
        """Gets the given time plus or minus the given shift.

        Args:
            timestamp (int): Timestamp formatted '%Y-%m-%d %H:%M:%S'.
            shift (int): Number of seconds plus or minus, e.g. 1 or -1.
    
        Returns:
            str: The shifted date and time.
        """
        secs = shift
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.datetime.strptime(timestamp, fmt)
        d2 = d1 + datetime.timedelta(seconds=secs)
        return str(d2)
        
    def dateshift(self, date:str, shift:int):
        """Gets the given date plus or minus the given shift.

        Args:
            date (str): Date string representation in format '%Y-%m-%d'.
            shift (int): Number of days plus or minus (e.g. 1 or -1).
    
        Returns:
            str: The shifted date.
        """
        fmt = '%Y-%m-%d'
        d1 = datetime.datetime.strptime(date, fmt)
        d2 = d1 + datetime.timedelta(days=shift)
        return str(d2)[:10]
        
    def timediff(self, timestamp1:str, timestamp2, unit:str):
        """Gets the difference between the given timestamps.

        Args:
            timestamp1 (str): Timestamp formatted '%Y-%m-%d %H:%M:%S'.
            timestamp2 (str): Second timestamp to compare.
            unit (str): Time unit second, minute, hour, day).
    
        Returns:
            int or float: The difference.
        """
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.datetime.strptime(timestamp1, fmt)
        d2 = datetime.datetime.strptime(timestamp2, fmt)
        sec = (d2-d1).total_seconds()
        diff = 0.0
        if unit == "day":
            diff = round((sec / 86400), 4)
        elif unit == "hour":
            diff = round((sec / 3600), 4)
        elif unit == "minute":
            diff = round((sec / 60), 4)
        else:
            diff = int(sec)
        return diff
