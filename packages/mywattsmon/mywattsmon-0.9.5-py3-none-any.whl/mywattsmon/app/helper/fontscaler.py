# -*- coding: utf-8 -*-
"""mywattsmon"""

import tkinter.font as tkfont

# ---------------------------------------------------------------
# Note concerning fonts
# ---------------------------------------------------------------
# A sans serif font such as DejaVu Sans is preferred. Tested on
# Raspberry Pi with Debian Linux: DejaVu Sans, DejaVu Sans Mono,
# Liberation Sans. 'Sans' is apparently converted to DejaVu Sans.
# Tested with Microsoft Windows: 'Sans' (was converted to Arial).
# ---------------------------------------------------------------
LABEL_FONT = "Sans"
LABEL_FONT_SIZE = 12
VALUE_FONT = "Sans"
VALUE_FONT_SIZE = 12
VALUE_FONT_SIZE_FROM = 8
VALUE_FONT_SIZE_TO = 800
VALUE_FONT_METRICS = "ascent"
VALUE_PAD = 30

class FontScaler:

    """
    FontScaler class.
    """

    def __init__(self):
        """Setup.

        Args:
            None.

        Returns:
            None.
        """
        self.width_valuefontsize_map = None
        self.width_valuefontsize_map_range = None
        self.height_valuefontsize_map = None
        self.height_valuefontsize_map_range = None
        self.__set_pixels_valuefontsize_map('w')
        self.__set_pixels_valuefontsize_map('h')

    def get_labelfont(self):
        """Gets the label font with persistent size value.
        
        Sets a negative size value for pixels (positive is for points).

        Args:
           None.

        Returns:
           object: A tkinter.font font object.
        """
        return tkfont.Font(family=LABEL_FONT, size=LABEL_FONT_SIZE * -1,
            weight='normal')
            
    def get_valuefont(self):
        """Gets the value font with start size value (will be resized).
        
        Sets a negative size value for pixels (positive is for points).

        Args:
           None.

        Returns:
           object: A tkinter.font font object.
        """
        return tkfont.Font(family=VALUE_FONT, size=VALUE_FONT_SIZE * -1,
            weight='normal')
            
    def get_valuegeometry(self, width:int, height:int):
        """Gets the value geometry.

        Args:
           width (int): Available width
           height (int): Available height

        Returns:
           int, int, int, int: value width, height, x, y.
        """
        vw = int(width - VALUE_PAD)
        vh = int(height - VALUE_PAD)
        vx = int(width / 2)
        vy = int((height / 2) + (VALUE_PAD / 4))
        return vw, vh, vx, vy
        
    def get_valuefontsize(self, width:int, height:int, text:str):
        """Gets the value font size for font scaling in pixels.

        Args:
           width (int): The value area width in pixels.
           height (int): The value area height in pixels.
           text (str): The value as string.

        Returns:
           int: The font size as negative value.
        """
        w = width
        h = height
        charcount = len(text)
        if charcount > 0:
            w = int(width / charcount) # For 1 character width map 
        if w < 1:
            w = 1
        if h < 1:
            h = 1
        wsize = self.__get_valuefontsize_for_pixels(w, 'w')
        hsize = self.__get_valuefontsize_for_pixels(h, 'h')
        if wsize < hsize:
            return wsize * -1 # Negative value for pixels
        else:
            return hsize * -1 # Negative value for pixels

    # ---------------
    # Private methods
    # ---------------
    
    def __set_pixels_valuefontsize_map(self, wh:str):
        """Sets a width-valuefontsize or height-valuefontsize map.
        
        A sans serif font such as DejaVu Sans is preferred.
        The width in pixels is set for a single character.

        Args:
           wh (str): 'w' for width-, 'h' for height-fontsize map.
        
        Returns:
           None.
        """
        if wh not in ('w', 'h'):
            return
        pixels_fontsize_map = {}
        lastpixels = 0
        font = tkfont.Font(family=VALUE_FONT, size=-12, weight='normal')
        for size in range(VALUE_FONT_SIZE_FROM, VALUE_FONT_SIZE_TO + 1):
            font.config(size=size * -1) # Negative value for pixels
            if wh == 'w':
                pixels = font.measure('0') # Single character
            else:
                pixels = font.metrics(VALUE_FONT_METRICS)
            if lastpixels == 0:
                lastpixels = pixels - 1
            if pixels == lastpixels + 1:
                lastpixels = pixels
                pixels_fontsize_map[pixels] = size
            else:
                # Fill pixels gap
                while pixels > lastpixels + 1:
                    lastpixels += 1
                    pixels_fontsize_map[lastpixels] = size
        pixelsfrom = list(pixels_fontsize_map.keys())[0]
        pixelsto = pixels
        if wh == 'w':
            self.width_valuefontsize_map = pixels_fontsize_map.copy()
            self.width_valuefontsize_map_range = [pixelsfrom, pixelsto]
        else:
            self.height_valuefontsize_map = pixels_fontsize_map.copy()
            self.height_valuefontsize_map_range = [pixelsfrom, pixelsto]
    
    def __get_valuefontsize_for_pixels(self, pixels:int, wh:str):
        """Gets the value font size for width or height pixels.

        Args:
           pixels (int): Width in pixels.
           height (int): Height in pixels.
           wh (str): 'w' for width-, 'h' for height pixels.
                   
        Returns:
           int: Font size for width or height pixels.
        """
        if wh not in ('w', 'h'):
            return -1
        fontsize = 0
        pixelsfrom = 0
        pixelsto = 0
        pixels_fontsize_map = None
        if wh == 'w':
            pixels_fontsize_map = self.width_valuefontsize_map
            pixelsfrom = self.width_valuefontsize_map_range[0]
            pixelsto = self.width_valuefontsize_map_range[1]
        else:
            pixels_fontsize_map = self.height_valuefontsize_map
            pixelsfrom = self.height_valuefontsize_map_range[0]
            pixelsto = self.height_valuefontsize_map_range[1]
        if pixels < pixelsfrom:
            fontsize = pixels_fontsize_map.get(pixelsfrom)
        elif pixels > pixelsto:
            fontsize = pixels_fontsize_map.get(pixelsto)
        else:
            fontsize = pixels_fontsize_map.get(pixels)
        return fontsize
