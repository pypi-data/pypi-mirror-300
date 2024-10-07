# **mywattsmon**

A minimal Python application for monitoring electrical power and energy in the smart home.

- Support for devices such as energy meters, smart plugs, etc.
- 24/7 monitor process with scheduled data storage
- Optional monitor window
- Low resource requirements
- Easily configurable via JSON file
- Extendable with your own device classes

A computer running Python version 3.11 or higher is required. For SBCs such as Raspberry Pi, a hard disk (e.g. a USB SSD) is recommended, as SD cards are generally not suitable for continuous operation.

## Installation

The application should be installed in a user directory, as it saves data and can be extended individually.

	python -m pip install mywattsmon -U -t <target directory> 

Alternatively, the release file can be downloaded from the respository and unpacked.

## Usage

In the following, it is assumed that the application has been installed on a Linux computer into the user's home directory (e.g. into /home/u1/mywattsmon) and that the calls are made from the home directory (/home/u1).

Start the monitor process (exit with Ctrl+C):

	python -m mywattsmon.app.monitor
    
Start the monitor window (exit with Ctrl+C, in the window using the exit button or escape key):

	python -m mywattsmon.app.window

*Note: When the application is started for the first time, the data directory mywattsmon-data is created parallel to the application directory. Among other things, this contains the configuration file config.json with a configuration of the device class Mock. As this class provides random numbers, the application can be executed directly after installation without further configuration.*

## Further information

- Documentation: /mywattsmon/doc/*
- Repository: https://github.com/berryunit/mywattsmon
- License: MIT
