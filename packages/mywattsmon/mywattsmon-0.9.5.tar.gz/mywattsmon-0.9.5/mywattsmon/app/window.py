# -*- coding: utf-8 -*-
"""mywattsmon"""

import argparse
import json
import os
import sys
import tkinter as tk

from mywattsmon.app.helper.fontscaler import FontScaler
from mywattsmon.app.helper.logger import Logger
from mywattsmon.app.helper.requester import Requester
from mywattsmon.app.helper.pathfinder import PathFinder
from mywattsmon.app.helper.timer import Timer

NONE_VALUE = "-"
OFF_VALUE = "~"
INVALID_VALUE = "v"
WARNING_VALUE = "w"
ERROR_VALUE = "x"
REFRESH_UNIT = "<refresh>"
INTERVALSTEP_SECONDS = 1

class Window():

    """
    Window class.
    """

    def __init__(self, datapath:str=None):
        """Setup.

        Args:
            datapath (str): This application's datapath, or None.

        Returns:
            None.
        """
        # Class name in lower case
        self.name = __class__.__name__.lower()

        # Path information
        pathinfo = PathFinder().get_pathinfo(datapath)
        configfile = pathinfo.get('configfile')
        datapath = pathinfo.get('datapath')

        # Configuration load
        with open(configfile, 'r') as f:
            config = json.load(f)
            
        # Listener port
        port = int(config['port'])

        # Logger
        loggerconfig = {}
        loggerconfig['datapath'] = datapath
        loggerconfig['loglevel'] = config['loglevel']
        loggerconfig['logtofile'] = config['logtofile']
        loggerconfig['logsource'] = self.name
        self.logger = Logger(loggerconfig)
        self.logger.log(0, f"Datapath: '{datapath}'")
        
        # Put out listener port
        self.logger.log(0, f"Listener port: {port}")

        # Requester
        self.requester = Requester(port, self.logger)

        # Timer
        timerconfig = {}
        timerconfig['interval'] = config["window"]["interval"]
        nightmode = config["window"]["nightmode"]
        timeframe = nightmode.get("timeframe")
        if timeframe is not None:
            timerconfig['nightmode_timeframe'] = timeframe
            ref = nightmode.get("colors")
            timerconfig['nightmode_colors'] = \
                config["window"]["colors"]["values"][ref]
        self.timer = Timer(timerconfig)
        self.interval = None
        self.intervalsteps = 0

        # Window configuration
        self.windowconfig = config["window"]

        # Window size options:
        # ------------------------------------------------
        # 'max' - full size window with frame
        # 'full' - without frame, close with Esc or Alt+F4
        # <Explicit setting> - w*h+x+y, e.g. '640x400+1+1'
        # ------------------------------------------------
        self.windowsize = self.windowconfig['size']
        
        # Window title and colors
        title = self.windowconfig['title']
        bg = self.windowconfig['colors']['window']['bg']
        
        # Tkinter root
        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(bg=bg)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        maxwidth, maxheight = self.root.maxsize()
        maxheight -= 40 # Reduce height slightly
        if self.windowsize == 'max':
            self.root.geometry(f"{maxwidth}x{maxheight}+0+0")
        elif self.windowsize == 'full':
            self.root.geometry(f"{screenwidth}x{screenheight}+0+0")
        else:
            self.root.geometry(self.windowsize)

        # Tkinter frame
        self.frame = tk.Frame(self.root, bg=bg, bd=2)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)

        # FontScaler instance
        self.fontscaler = FontScaler()
        
        # Canvas for refresh countdown
        self.refresh_widget = None

        # Create the grid on the frame
        self.frame.widgets = self.__create_grid(self.windowconfig['grid'])
        
        # Bind Escape to root (for fullscreen)
        self.root.bind('<Escape>', self.stop_process)

        # Window resizing
        self.root.after(100, self.__resize_font)
        self.root.after(500, self.__delay_resize_config)
        
        # Window refresh
        self.root.after(1000, self.__refresh)

    def process(self):
        """The main window process, i.e. the tkinter root.mainloop.
        
        Can be stopped via KeyboardInterrupt, also under Windows.
        
        Args:
           None.
                   
        Returns:
            int: 0=regular, 1=irregular end of the process.
        """
        eop = 0
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.log(0, "Close request received.")
        except:
            eop = 1
            self.logger.log(1, "Error in window process.")
        finally:
            self.__close()
        self.logger.log(0, "End of window process. Bye")
        return eop
        
    def stop_process(self, event:object=None):
        """Stops the process, i.e. the tkinter root.mainloop.
         
        Args:
           event (object): An arbitrary event, or None.
        
        Returns:
           None
        """
        self.root.destroy()

    # ---------------
    # Private methods
    # ---------------
    
    def __close(self):
        """Closes resources.
         
        Args:
           None.
        
        Returns:
           None
        """
        try:
            self.logger.log(0, "Closing requester ...")
            self.requester.close()
        except:
            self.logger.log(1, "Could not close requester.")

    def __refresh(self):
        """Refreshes the window in interval steps by recursive call.

        Args:
           None.
                   
        Returns:
           None.
        """
        try:
            if self.intervalsteps <= 1:
                # Request
                self.__set_refresh_countdown(0)
                data = self.requester.request()
                if data is not None:
                    self.__set_current_values(data)
                # Get and set interval
                self.interval = self.timer.get_interval()
                seconds = self.interval['seconds']
                self.intervalsteps = int(seconds / INTERVALSTEP_SECONDS)
            else:
                self.intervalsteps -= 1 # Decrement
            self.__set_refresh_countdown(self.intervalsteps)
            self.root.after(INTERVALSTEP_SECONDS*1000, self.__refresh)
        except:
            self.logger.log(1, "Error at window refresh.")
            self.stop_process()

    def __create_grid(self, gridconfig):
        """Creates the grid on the frame and returns the widgets.
         
        Args:
           gridconfig (dict): The grid configuration.
        
        Returns:
           dict: Widgets configuration, objects, references.
        """
        gridinfo = self.__get_gridinfo(gridconfig)
        widgets = {}
        widgetcount = 0
        maxrownum = 0
        maxcolnum = 0
        for widgetnum in gridinfo:
            widget = gridinfo[widgetnum]
            text = widget['text'].strip()
            rownum = widget['rownum']
            colnum = widget['colnum']
            rowspan = widget['rowspan']
            colspan = widget['colspan']
            bg = widget['bg+']
            fg = widget['fg+']
            # Canvas
            canvas = tk.Canvas(self.frame, bg=bg, width=1, height=1,
            borderwidth=0, highlightthickness=0) 
            # Label
            labelfont = self.fontscaler.get_labelfont()
            labelid = canvas.create_text(4, 4, anchor='nw',
                text=text, fill=fg, font=labelfont)
            # Value
            valuefont = self.fontscaler.get_valuefont()
            valueid = canvas.create_text(1, 1, anchor = 'c',
                text=NONE_VALUE, fill=fg, font=valuefont)
            # Canvas on grid
            canvas.grid(sticky=tk.NSEW,
                row=rownum, column=colnum,
                rowspan=rowspan, columnspan=colspan,
                padx=4, pady=4
                )
            # Widget
            widget['name'] = canvas._name
            widget['canvas'] = canvas
            widget['labelid'] = labelid
            widget['labelfont'] = labelfont
            widget['valueid'] = valueid
            widget['valuefont'] = valuefont
            widgets[canvas._name] = widget
            # Set max row and column numbers for grid scaling
            if maxrownum < rownum:
                maxrownum = rownum
            if maxcolnum < colnum:
                maxcolnum = colnum
            # Set the canvas for refresh countdown
            if widget['units'] == REFRESH_UNIT:
                self.refresh_widget = {}
                self.refresh_widget['name'] = canvas._name
                self.refresh_widget['canvas'] = canvas
                self.refresh_widget['valueid'] = valueid
        # Add weight to widgets for grid scaling
        for rownum in range(maxrownum + 1):
            tk.Grid.rowconfigure(self.frame, rownum, weight=1)
        for colnum in range(maxcolnum + 1):
            tk.Grid.columnconfigure(self.frame, colnum, weight=1)
        # Return widgets
        return widgets
        
    def __get_gridinfo(self, gridconfig):
        """Gets specifc grid information from grid configuration.
         
        Args:
           gridconfig (dict): The grid configuration.
        
        Returns:
           dict: The grid information.
        """
        gridinfo = {}
        widgetnum = 0
        for widgetname in gridconfig:
            widgetnum += 1
            widget = gridconfig[widgetname]
            widget['text'] = widgetname
            colors = self.__get_valuecolors(widget['colors'])
            widget['bg+'] = colors['bg+']
            widget['fg+'] = colors['fg+']
            widget['bg-'] = colors['bg-']
            widget['fg-'] = colors['fg-']
            gridinfo[widgetnum] = widget
        return gridinfo
        
    def __get_valuecolors(self, refkey:str):
        """Gets value colors by the configured reference.
         
        Args:
           refkey (str): Key of the color reference.
        
        Returns:
           dict: The configured colors.
        """
        colors = {}
        config = self.windowconfig['colors']['values']
        bg_plus = config[refkey].get('bg+')
        fg_plus = config[refkey].get('fg+')
        bg_minus = config[refkey].get('bg-')
        fg_minus = config[refkey].get('fg-')
        if bg_plus is None:
            bg_plus = config[refkey].get('bg')
        if fg_plus is None:
            fg_plus = config[refkey].get('fg')
        if bg_minus is None:
            bg_minus = config[refkey].get('bg')
        if fg_minus is None:
            fg_minus = config[refkey].get('fg')
        colors['bg+'] = bg_plus
        colors['fg+'] = fg_plus
        colors['bg-'] = bg_minus
        colors['fg-'] = fg_minus
        return colors

    def __delay_resize_config(self):
        """Sets root attributes and binds the resize event method.
        
        Sets the attributes 'zoomed' and 'fullscreen' with
        delay, as an active window appears to be required.
         
        Args:
           None.
        
        Returns:
           None.
        """
        if self.windowsize == "max":
            try:
                self.root.attributes('-zoomed', True)
            except:
                self.root.state('zoomed')
        elif self.windowsize == "full":
            self.root.attributes('-fullscreen', True)
        else:
            pass # Explicit size setting assumed
        if self.windowsize != "full":
            self.root.bind('<Configure>', self.__resize)
            
    def __resize(self, event):
        """Invokes font resizing for canvas widgets.
         
        Args:
           None.
        
        Returns:
           None
        """
        source = str(event.widget)
        if source.find('canvas') > 0:
            self.__resize_font(event.widget._name)
        
    def __resize_font(self, widget_name:str=None):
        """Handles font resizing for canvas widgets.
         
        Args:
           None.
        
        Returns:
           None
        """
        widget_names = []
        if widget_name is None:
            for name in self.frame.widgets:
                widget_names.append(name)
        else:
            widget_names.append(widget_name)
        for name in widget_names:
            widget = self.frame.widgets[name]
            canvas = widget['canvas']
            vw, vh, vx, vy = self.fontscaler.get_valuegeometry(
                canvas.winfo_width(), canvas.winfo_height()
                )
            vid = widget['valueid']
            vfont = widget['valuefont']
            vtext = canvas.itemcget(vid, "text")
            vfont.config(
                size=self.fontscaler.get_valuefontsize(vw, vh, vtext)
                )
            canvas.coords(vid, vx, vy)
        
    def __set_current_values(self, current_values:dict):
        """Sets current power and energy values to the window.

        Args:
           current_values (dict): Current values from the monitor.
 
        Returns:
           None.
        """
        for widget in self.frame.widgets:
            # Get required widget data
            units = self.frame.widgets[widget].get('units')
            var = self.frame.widgets[widget].get('var')
            bg_plus = self.frame.widgets[widget].get('bg+')
            fg_plus = self.frame.widgets[widget].get('fg+')
            bg_minus = self.frame.widgets[widget].get('bg-')
            fg_minus = self.frame.widgets[widget].get('fg-')
            labelid = self.frame.widgets[widget].get('labelid')
            valueid = self.frame.widgets[widget].get('valueid')
            canvas = self.frame.widgets[widget].get('canvas')
            # Handle values
            value1 = str(canvas.itemcget(valueid, 'text'))
            value2 = \
                self.__get_value_for_widget(units, var, current_values)
            if value1 != value2:
                canvas.itemconfig(valueid, text=value2)
                canvas.update()
                if len(value1) != len(value2):
                    self.logger.log(3, f"Resizing {widget}")
                    self.__resize_font(widget)
            # Handle colors
            bg = str(canvas.cget('bg'))
            fg = str(canvas.itemcget(labelid, 'fill'))
            bg2 = bg
            fg2 = fg
            nightmode_colors = self.timer.get_nightmode_colors()
            if nightmode_colors is not None:
                bg2 = nightmode_colors['bg']
                fg2 = nightmode_colors['fg']
            else:
                bg2 = bg_plus
                fg2 = fg_plus
                if value2.replace('-', '').replace('.', '').isnumeric():
                    if float(value2) < 0:
                        bg2 = bg_minus
                        fg2 = fg_minus
            if bg != bg2 or fg != fg2:
                canvas.config(bg=bg2)
                canvas.itemconfig(labelid, fill=fg2)
                canvas.itemconfig(valueid, fill=fg2)
                canvas.update()

    def __get_value_for_widget(self, units:str, var:str, values:dict):
        """Gets a power or energy value from the given unit or unit list.
        
        If a unit list is given, the values are summed up.

        Args:
           units (str): Unit name or CSV list of unit names.
           var (str): Configured variable. Options: 'power', 'energy'.
           values (dict): Current values of all units.
 
        Returns:
           str: The value as string.
        """
        value = 0
        unitlist = units.replace(' ', '').split(',')
        for unit in unitlist:
            if values.get(unit) is None:
                return NONE_VALUE # No values at all
            code = values[unit].get('code')
            if code is None:
                return NONE_VALUE # No code
            if code == 1:
                return ERROR_VALUE # Error, see log
            if code == 2:
                state = values[unit].get('state')
                if state is not None and state == 'OFF':
                    return OFF_VALUE # Unit is off
                else:
                    return WARNING_VALUE # Warning, see log
            val = values[unit].get(var)
            if val is None:
                return NONE_VALUE # No value
            if type(val) not in (int, float):
                return INVALID_VALUE # Type int or float required
            value += val
        return str(value)

    def __set_refresh_countdown(self, countdown:int):
        """Sets the given countdown value to the refresh widget.
         
        Args:
           countdown (int): The current countdown value.
        
        Returns:
           None.
        """
        if self.refresh_widget is None:
            return
        canvas = self.refresh_widget['canvas']
        valueid = self.refresh_widget['valueid']
        value1 = str(canvas.itemcget(valueid, 'text'))
        value2 = str(countdown)
        canvas.itemconfig(valueid, text=str(countdown))
        if len(value1) != len(value2):
            self.logger.log(3, f"Resizing refresh countdown")
            self.__resize_font(self.refresh_widget['name'])
        canvas.update()

# ----
# Main
# ----

def main(args):
    parser = argparse.ArgumentParser(
    description="WINDOW process.",
    usage="python -m mywattsmon.app.window [-h,--help] [-d,--datapath]")
    parser.add_argument('-d', '--datapath', type=str,
        default="mywattsmon-data",
        help="e.g. 'mywattsmon-data', or an absolute path")
    args = parser.parse_args()
    print("  ============================================")
    print("  WINDOW process. Close with Ctrl+C, or on the")
    print("  window with the Cancel button or Escape key.")
    print("  ============================================")
    window = Window(args.datapath)
    return window.process()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
