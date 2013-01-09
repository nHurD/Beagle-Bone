#!/usr/bin/python 
##################################################################
## Temperature.py                                               ##
## A simple class to read from a DS1820 digital thermometer     ##
##################################################################
## Application usage:                                           ##
## usage: Temperature.py [-h] [-m] [-f] sensor_id               ##
##                                                              ##
##    positional arguments:                                     ##
##      sensor_id        The id of the sensor to read           ##
##                                                              ##
##    optional arguments:                                       ##
##      -h, --help       show this help message and exit        ##
##      -m, --monitor    Monitor the sensor continuously        ##
##      -f, --farenheit  Display units in Farenheit rather than ## 
##                       Celcius                                ##
##################################################################

import re



class Temperature:
    """
    Temperature class to read data from the w1 bus on the board 
    The class takes one argument at instantiation: The id of the sensor
    """

    __sensor_path__ = '/sys/bus/w1/devices/{0}/w1_slave'

    def open_sensor(self):
        if (self.sensor_id == ''):
            return
        try:
            self.sensor = open(self.__sensor_path__.format(self.sensor_id),'r')
        except IOError:
            print 'Unable to open {0} for reading'.format(self.sensor_id)
            sys.exit(1)

    def close_sensor(self):
        self.sensor.close()

    def GetTemperature(self, in_fahrenheit=False):
        self.open_sensor()

        self.current_temp = float(re.findall('\d+$',self.sensor.readlines()[1])[0])/1000

        self.close_sensor()

        if (not in_fahrenheit):
            return self.current_temp
        else:
            return (1.8 * self.current_temp) + 32

    def __init__(self, sensor_id):
        self.sensor_id = sensor_id

if __name__ == '__main__':

    import argparse
    import sys
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument('sensor_id', help="The id of the sensor to read")
    parser.add_argument('-m',
            '--monitor',
            help="Monitor the sensor continuously",
            action="store_true")
    parser.add_argument('-f',
            '--farenheit',
            help="Display units in Farenheit rather than Celcius",
            action="store_true")
    
    args = parser.parse_args()

    display_temperature = lambda x: "{0:.2f} deg {1}".format(x, ("F" if args.farenheit else "C"))

    temp_sensor = Temperature(args.sensor_id)
    print "Monitoring sensor {0}".format(args.sensor_id)

    if (args.monitor):
        while(1):
            try:
                print '\r',
                T = temp_sensor.GetTemperature(args.farenheit)
                print display_temperature(T),
                sys.stdout.flush()
                print '\r',
            except KeyboardInterrupt:
                sys.exit(0)
    else:
        T = temp_sensor.GetTemperature(args.farenheit)
        print display_temperature(T)
