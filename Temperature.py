#!/usr/bin/python 

import re


class Temperature:
    __sensor_path__ = '/sys/bus/w1/devices/{0}/w1_slave'

    def open_sensor(self):
        if (self.sensor_id == ''):
            return
        try:
            self.sensor = open(self.__sensor_path__.format(self.sensor_id),'r')
        except IOError:
            print 'Unable to open {0} for reading'.format(self.sensor_id)

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

    temp_sensor = Temperature(args.sensor_id)
    if (args.monitor):
        while(1):
            try:
                T = temp_sensor.GetTemperature(args.farenheit)
                print "Current Temperature: {0:.2f} deg {1}".format(T, 
                        ('F' if args.farenheit else 'C')
                ),
                time.sleep(1)
                sys.stdout.flush()
                print '\r',
            except KeyboardInterrupt:
                sys.exit(0)
