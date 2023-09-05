from labjack import ljm
from datetime import datetime
import sys
from abc import ABC, abstractmethod, abstractproperty

class Sensor(ABC):
    def setChannel(self, device:str, sensor_name:str, channel:str):
        '''Sets the channel information'''
        self.device = device # labjack fandler
        self.channel = channel # AINx of labjack
        self.sensor_name = sensor_name # sensor name
        return self

    @property
    def voltage(self) -> float:
        '''labjack voltage'''
        u = round(ljm.eReadName(self.device, self.channel),4)
        if -0.5 < u < 0: u = 0
        elif u < -0.5: raise ValueError('negative input voltage')
        return u

    @abstractproperty
    def value(self):
        '''aquired physical value'''
        pass

    @abstractproperty
    def unit(self) -> str:
        '''physical unit'''
        pass

    def __repr__(self) -> str:
        '''representation of sensor e.g.: T1 = 25.1°C '''
        if isinstance(self.value, float):
            return f'{self.sensor_name}:\t{self.value:.1f}{self.unit}'
        else:
            return f'{self.sensor_name}:\t{self.value}'
    
class PT100(Sensor):
    ''' PT100 sensor
        T_min -> Temperature in Grad Celsius for 0V
        T_max -> Temperature in Grad Celsius for 10V '''
    def __init__(self, T_min:int = 0, T_max:int = 150) -> None:
        super().__init__()
        self.T_min = T_min
        self.T_max = T_max
    
    @property
    def unit(self) -> str:
        return '°C'

    @property
    def value(self) -> float:
        ''''temperature in Grad Celsius'''
        k = (self.T_max - self.T_min) / 10 # slope
        d = self.T_min # offset
        return round(k * self.voltage + d, 4)

class Flowmeter(Sensor):
    '''IFM Flowmeter
        mDot_min -> massflow in ml/min for 4mA
        mDot_max -> massflow in ml/min for 20mA'''
    def __init__(self, R_shunt:int = 470, mdot_min:int = 0, mdot_max: int = 2000) -> None:
        super().__init__()
        self.R_shunt = R_shunt
        self.mdot_min = mdot_min
        self.mdot_max = mdot_max

    @property
    def unit(self) -> str:
        return 'ml/s'

    @property
    def value(self) -> float:
        ''''massflow in ml/s'''
        k = (self.mdot_max-self.mdot_min)/(16*1e-3) # slope
        d = self.mdot_min - k*4*1e-3 # offset

        I = self.voltage/self.R_shunt # current
        if I < 4*1e-3: I = 4*1e-3 # correct no flow
        return round((k*I + d)/60, 2)

class Switch(Sensor):

    def __init__(self) -> None:
        super().__init__()

    @property
    def unit(self) -> str:
        return '[1]'

    @property
    def value(self) -> str:
        ''''logic true/false'''
        if self.voltage <= 1: # cold
            return 'cold'
        else: # warm
            return 'warm'

class MeasurementData():
    '''managing all sensors connected to the labjack device and configured by a yaml file'''
    def __init__(self, device: ljm, configFile: str) -> None:
        self.sensors = [] # list with all connected sensors [PT100, Flowmeter, Switch]

        with open(configFile, "r") as ymlfile:
            labjackConfiguration = yaml.safe_load(ymlfile)
        
        for sensorType in labjackConfiguration:
            # PT100, Flowmeter, Switch
            for name, channel in sensorType:
                sensor = getattr(sys.modules[__name__], sensorType)
                sensor.setChannel(device, name, channel)
                self.sensors.append(sensor)
        

if __name__ == '__main__':
    # Test classes
    import yaml
    with open('labjack.yml', "r") as ymlfile:
            labjackConfiguration = yaml.safe_load(ymlfile)
    print(labjackConfiguration['PT100'].keys())

    labjackT7Pro = ljm.openS("T7", "USB", "ANY")






            
    