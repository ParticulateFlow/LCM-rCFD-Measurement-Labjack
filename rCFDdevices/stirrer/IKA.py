import serial
import serial.tools.list_ports

class IKA_Ministar40():
    '''Control class for the IKA ministar 40'''
    def __init__(self, port: str, speedLimit: int) -> None:

        print("+ IKA Ministar 40")

        # Find right port
        portObjects = serial.tools.list_ports.comports() #all available Ports
        nameList = [portObjects[i].description for i in range(len(portObjects))]
        try:
            index = [idx for idx, s in enumerate(nameList) if port in s][0]
            self.device = portObjects[index].name

            self.reset()
            self.set_speedLimit(speedLimit + 1)
            print(f"++ Stirrer found on Port {portObjects[index].name}")
            print("++ Device ready to use")
        except:
            print("++ Stirrer not connected")
            print('++ Debug Mode on')
            self.device = None

    @property
    def deviceName(self) -> str:
        '''read device name'''
        return self._readCommand('IN_NAME \r\n')
    
    @property
    def PT1000(self) -> float:
        '''Read PT1000 value'''
        return 
    
    @property
    def currentSpeed(self) -> int:
        '''Read current speed value'''
        val = self._readCommand('IN_PV_4 \r\n')
        if not val:
            val = 0
        else:
            return int(float(val))

    @property
    def currentTorque(self) -> float:
        '''Read current torque value'''
        return float(self._readCommand('IN_PV_5 \r\n'))

    @property
    def ratedSpeed(self) -> int:
        '''Read rated speed value'''
        return int(float(self._readCommand('IN_SP_4 \r\n')))

    @property
    def torqueLimit(self) -> float:
        '''Read the torque limit value'''
        return float(self._readCommand('IN_SP_5 \r\n'))
        
    @property
    def speedLimit(self) -> int:
        '''Read the speed limit value'''
        return int(float(self._readCommand('IN_SP_6 \r\n')))

    @property
    def safetyLimit(self) -> int:
        '''Read the safety speed value'''
        return int(float(self._readCommand('IN_SP_8 \r\n')))
    
   
    def set_ratedSpeed(self, rpm: int) -> None:
        '''Adjust the rated speed value'''
        self._writeCommand(f'OUT_SP_4 {rpm}\r\n')

    def set_torqueLimit(self, torque: float) -> None:
        '''Adjust the torque limit value'''
        self._writeCommand(f'OUT_SP_5 {torque}\r\n')

    def set_speedLimit(self, rpmLimit: int) -> None:
        '''Adjust the speed limit value'''
        self._writeCommand(f'OUT_SP_6 {rpmLimit}\r\n')

    def set_safetyLimit(self, safetyLimit: int) -> None:
        '''Adjust the safety speed value'''
        self._writeCommand(f'OUT_SP_8 {safetyLimit}\r\n')
    
    def start(self) -> None:
        '''Start the motor'''
        self._writeCommand('START_4 \r\n')          
                           
    def stop(self) -> None:
        '''Stop the motor'''
        self._writeCommand('STOP_4 \r\n')        

    def reset(self) -> None:
        '''Switch to normal operating mode'''
        self._writeCommand('RESET_4 \r\n')        

    @property
    def direction_right(self) -> None:
        '''right direction'''
        self._writeCommand(f'OUT_MODE_1 \r\n' )

    @property
    def direction_left(self) -> None:
        '''left direction'''
        self._writeCommand(f'OUT_MODE_2 \r\n' )

    @property
    def direction(self):
        '''Read the direction of rotation'''
        return self._readCommand('IN_MODE \r\n')

    def _readCommand(self, command: str):
        if not self.device:
            print("Read Command")
            print(command)
            return
        
        try:
            with serial.Serial(self.device, '9600', timeout=1) as ser:
                ser.write(command.encode("ascii"))
                val = ser.readline().decode("ascii")
                if ' ' in val:
                    val = val.split()
                    return val[0]
                else:
                    return val
        except:
            return None

    def _writeCommand(self, command: str) -> None:
        if not self.device:
            print("Write Command")
            print(command)
            return


        try:
            with serial.Serial(self.device, '9600', timeout=1) as ser:
                ser.write(command.encode("ascii"))
                _ = ser.readline().decode("ascii")
        except:
            print('Cannot write command')

if __name__ == '__main__':
    IKA_Ministar40(port='COM9', speedLimit=120)


