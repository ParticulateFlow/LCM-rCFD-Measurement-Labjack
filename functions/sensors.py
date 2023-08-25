from labjack import ljm
from abc import ABC, abstractmethod, abstractproperty

class Sensors(ABC):
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
        '''transformation of sensor data'''
        pass

    @abstractproperty
    def unit(self) -> str:
        '''Physical unit of sensor'''
        pass

    def __repr__(self) -> str:
        '''representation of sensor e.g.: T1 = 25.1°C '''
        if isinstance(self.value, float):
            return f'{self.sensor_name} = {self.value:.1f}{self.unit}'
        if isinstance(self.value, bool):
            if self.value:
                return f'{self.sensor_name} = warm'
            else:
                return f'{self.sensor_name} = cold'
    
class PT100(Sensors):
    ''' PT100 sensor
        T_min -> Temperature in Grad Celsius for 0V
        T_max -> Temperature in Grad Celsius for 10V '''
    def __init__(self, T_min:int = 0, T_max:int = 150) -> None:
        super().__init__()
        self.T_min = T_min
        self.T_max = T_max
    
    @property
    def unit(self) -> str:
        return chr(176)+'C'

    @property
    def value(self) -> float:
        ''''temperature in Grad Celsius'''
        k = (self.T_max - self.T_min) / 10 # slope
        d = self.T_min # offset
        return round(k * self.voltage + d, 4)

class Flowmeter(Sensors):
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
        return 'ml/min'

    @property
    def value(self) -> float:
        ''''massflow in ml/min'''
        k = (self.mdot_max-self.mdot_min)/(16*1e-3) # slope
        d = self.mdot_min - k*4*1e-3 # offset

        I = self.voltage/self.R_shunt # current
        if I < 4*1e-3: I = 4*1e-3 # correct no flow
        return round(k*I + d, 4)

class Switch(Sensors):

    def __init__(self) -> None:
        super().__init__()

    @property
    def unit(self) -> str:
        return '[1]'

    @property
    def value(self) -> bool:
        ''''logic true/false'''
        if self.voltage <= 1: # False
            return False
        else:
            return True


if __name__ == '__main__':
    # Test classes
    from labjack import ljm
    labjackT7Pro = ljm.openS("T7", "USB", "ANY")

    def test_sensor(s: Sensors) -> None:
        print(f"Voltage = {s.voltage}")
        print(f"Value = {s.value}")
        print(f"Unit = {s.unit}")
        print("Representation:")
        print('-'*15)
        print(s)
        print("")


    print('PT100 - Class'.upper())
    print("+"*30)
    S1 = PT100().setChannel(device=labjackT7Pro, sensor_name='T_warm', channel='AIN0')
    print(ljm.eReadName(labjackT7Pro, 'AIN0'))
    test_sensor(S1)

    print('Flowmeter - Class'.upper())
    print("+"*30)
    S2 = Flowmeter().setChannel(device=labjackT7Pro, sensor_name='warm_massflow', channel='AIN11')
    print(ljm.eReadName(labjackT7Pro, 'AIN11'))
    test_sensor(S2)


    print('Switch - Class'.upper())
    print("+"*30)
    S3 = Switch().setChannel(device=labjackT7Pro, sensor_name='warm/cold', channel='AIN10')
    print(ljm.eReadName(labjackT7Pro, 'AIN10'))
    test_sensor(S3)


            
    