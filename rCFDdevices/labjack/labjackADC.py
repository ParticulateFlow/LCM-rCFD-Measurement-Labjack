from labjack import ljm
from datetime import datetime
from .sensors import *
import yaml
from dataclasses import dataclass
from pathlib import Path

@dataclass
class labjackConfiguration():
    device: str # T7 or T4
    connection: str # USB or Ethernet
    identifier: str


class ADC():
    '''managing all sensors connected to the labjack device and configured by a yaml file'''
    def __init__(self, ljmConf: labjackConfiguration) -> None:
        print("+ Labjack ADC")
        try:
            labjack = ljm.openS(
                ljmConf.device,
                ljmConf.connection,
                ljmConf.identifier)
            print(f"++ Labjack {ljmConf.device} connected via {ljmConf.connection}")
        except:
            print(f"++ Cannot open Labjack {ljmConf.device} via {ljmConf.connection}")
            print("++ Debug mode on")
            labjack = None

        
        # open configuration file
        p = Path(__file__).with_name('sensorConfig.yml')
        with open(p, "r") as ymlfile:
            labjackConfiguration = yaml.safe_load(ymlfile)

        self.sensors = [] # list with all connected sensors [PT100, Flowmeter, Switch]
        for sensorType in labjackConfiguration:
            # PT100, Flowmeter, Switch
            # sensCls is the sensor object
            # sens is an instance
            for name, channel in labjackConfiguration[sensorType].items():
                sensCls = eval(sensorType) 
                sens = sensCls()
                sens.setChannel(device=labjack, channel=channel, name=name)
                self.sensors.append(sens)

    @property
    def data(self) -> dict:
        '''aquired data as dict'''
        d = {'timestamp': datetime.now().isoformat()} #strftime('%Y%m%d_%H%M%S_%f')

        for sensor in self.sensors:
            d[sensor.name] = sensor.value
        return d
        

if __name__ == '__main__':
    # Test classes
    conf = labjackConfiguration(
        device='T7',
        connection='ETHERNET',
        identifier='ANY'
    )

    adc = ADC(ljmConf=conf)
    print(adc.data)
