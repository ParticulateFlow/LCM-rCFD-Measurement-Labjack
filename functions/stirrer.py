import serial
import serial.tools.list_ports

class IKA_Ministar40():
    '''Control class for the IKA ministar 40'''
    def __init__(self,usbName:str, speedLimit: int) -> None:
        # Find right port
        ports = serial.tools.list_ports.comports() #all available Ports
        nameList = [ports[i].description for i in range(len(ports))]
        try:
            index = [idx for idx, s in enumerate(nameList) if usbName in s][0]
        except:
            raise ConnectionError("Device not connected")

        print("Device found:")
        print(f"{ports[index].name}:{ports[index].description}")
        self.device = ports[index].name

        self.reset()
        self.set_speedLimit(speedLimit)

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
        return int(float(self._readCommand('IN_PV_4 \r\n')))

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
        '''Adjust the safety spped value'''
        self._writeCommand(f'OUT_SP_8 {safetyLimit}\r\n')
    
    def start(self) -> None:
        '''Start the motor'''
        self._writeCommand('START_4 \r\n')
        val = self.ratedSpeed              
                           
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

    def _readCommand(self, command: str) -> str:
        with serial.Serial(self.device, '9600', timeout=1) as ser:
            ser.write(command.encode("ascii"))
            val = ser.readline().decode("ascii")
            if ' ' in val:
                val = val.split()
                return val[0]
            else:
                return val

    def _writeCommand(self, command: str) -> None:
        with serial.Serial(self.device, '9600', timeout=1) as ser:
            ser.write(command.encode("ascii"))
            _ = ser.readline().decode("ascii")
        

import tkinter as tk
from tkinter import ttk
        
class Frame_Stirrer(tk.Frame):
    def __init__(self, parent, stirrer: IKA_Ministar40):
        super().__init__(master=parent)
        self.stirrer = stirrer

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.columnconfigure((0,1), weight=1)
        
        # first column
        ttk.Label(self, text=f'Stirrer Control \n {self.stirrer.deviceName}', font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2)
        self.scale = ttk.Scale(self,
                               from_= 30, to=self.stirrer.speedLimit, value=60, 
                               command=lambda event: self.label.config(text=f"{int(self.scale.get())} U/min") ,
                               orient='vertical', length=150)
        self.scale.bind("<ButtonRelease-1>",
                        lambda event: self.stirrer.set_ratedSpeed(int(self.scale.get())))
        self.scale.grid(row=1, column=0, padx=20, pady=20)
        self.label = ttk.Label(self, text=f"{int(self.scale.get())} U/min")
        self.label.grid(row=2, column=0)

        # second column
        self.control = tk.Frame(self)
        ttk.Button(self.control, text='Start', command=self.start). pack()
        ttk.Button(self.control, text='Stop', command=self.stirrer.stop).pack()
        ttk.Button(self.control, text='Reset Stirrer', command=self.stirrer.reset).pack()
        #ttk.Button(self.control, text='Read RPM', command=self.stirrer.readRPM).pack()
        self.control.grid(row=1, column=1, columnspan=2)
    
    def start(self):
        val = int(self.scale.get())
        self.stirrer.start()
        self.stirrer.set_ratedSpeed(val)


if __name__ == "__main__":
    stirrer = IKA_Ministar40(usbName = 'USB', speedLimit=120)
    window = tk.Tk()
    window.title('rCFD Experiment')
    Frame_Stirrer(window, stirrer=stirrer).pack()
    window.mainloop()


