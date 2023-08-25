if __name__ == '__main__':
    from config import Configuration
    from sensors import PT100, Flowmeter, Switch
    from periodicHandler import periodicFunctionHandler
else:
    from .config import Configuration
    from .sensors import PT100, Flowmeter, Switch
    from .periodicHandler import periodicFunctionHandler

from labjack import ljm
from datetime import datetime
import os
from datetime import datetime
from pathlib import Path

class MeasurementDataHandler():
    '''handler for managing all sensors connected to the labjack device and configured by a yaml file'''
    def __init__(self, device:ljm, configuration: Configuration) -> None:
        self.device = device
        self.conf = configuration
        self.SENSOR_LIST = {}
        def appendSensorCategory(Category: str, sensorClass) -> None:
            for name, ch in self.conf.labjack[Category].items():
                s = sensorClass()
                s.setChannel(device = self.device, sensor_name = name, channel = ch)
                self.SENSOR_LIST[name] = s
        appendSensorCategory('PT100', PT100)
        appendSensorCategory('Flowmeter', Flowmeter)
        appendSensorCategory('Switch', Switch)

        self.sensor_names = [s for s in self.SENSOR_LIST.keys()]
        self.sensor_names.insert(0, 'timestamp')

    def getSensorByName(self, name):
        return self.SENSOR_LIST[name]

    @property
    def sample_rate(self) -> int:
        '''sample rate in sample/seconds'''
        return int(self.conf.experiment['SAMPLE_RATE'])
    
    @property
    def inlet_conf(self) -> str:
        return self.conf.experiment['INLET']

    @property
    def outlet_conf(self) -> str:
        return self.conf.experiment['OUTLET']

    @property
    def timestamp(self):
        '''timestamp of aquired data'''
        return datetime.now()

    def printCMD(self) -> str:
        '''print all sensor data to the command'''
        data = self.SENSOR_LIST.values()
        [print(s) for s in data]
        # Go with cursor up
        print(f"\r\033[{len(data)}A", end="")

    def all_sensor_values(self) -> list:
        '''returns the measured data as a list with timestamp'''
        data = [s.value for s in self.SENSOR_LIST.values()]
        data.insert(0, self.timestamp.strftime('%Y%m%d_%H%M%S_%f'))
        return data
    
if __name__ == '__main__':
    from config import Configuration

    labjack = ljm.openS("T7", "USB", "ANY") # labjack T7 Pro
    config = Configuration(pathToConfigFiles=Path(__file__).parent.parent.absolute() / 'configs')
    mdh = MeasurementDataHandler(device=labjack, configuration=config)

    mdh.printCMD()

    print('\n Sensor Class')
    sensor = mdh.getSensorByName(name='Twarm')
    print(type(sensor))
    print(sensor)