import tkinter as tk
from tkinter import ttk

from functions.config import Configuration
from functions.measurementHandler import MeasurementDataHandler
from functions.experimentHandler import ExperimentHandler
from functions.sensors import PT100, Flowmeter

from labjack import ljm

from pathlib import Path





class Frame_aquisitionControl(tk.Frame):
    def __init__(self, parent, handler: ExperimentHandler):
        super().__init__(master=parent, highlightbackground="gray", highlightthickness=1)

        self.grid_rowconfigure((0,1), weight=2, uniform='a')
        self.grid_columnconfigure((0,1), weight=1, uniform='a')

        label = ttk.Label(self, text='Aquisition Control', font=('Arial', 14))
        bStart = ttk.Button(self, text='Start', command=handler.start)
        bStop = ttk.Button(self, text='Stop', command=handler.stop)

        label.grid(row=0, column=0, columnspan=2, pady=5, sticky='')
        bStart.grid(row=1,column=0)
        bStop.grid(row=1, column=1)

class Frame_massflow(tk.Frame):
    def __init__(self, parent, name:str, mDot_Sensor: Flowmeter, T_Sensor: PT100):
        super().__init__(master=parent, highlightbackground="gray", highlightthickness=1)
        self.mDot_Sensor = mDot_Sensor
        self.T_Sensor = T_Sensor

        self.grid_rowconfigure((0,1,2), weight=2, uniform='a')
        self.grid_columnconfigure((0,1), weight=1, uniform='a')

        self.mDot_var = tk.DoubleVar()
        self.T_var = tk.DoubleVar()

        ttk.Label(self,text=name, font=('Arial', 12, 'bold')).grid(row=0,column=0, columnspan=2)

        ttk.Label(self, text=self.mDot_Sensor.sensor_name).grid(row=1, column=0)
        ttk.Label(self, textvariable=self.mDot_var).grid(row=2, column=0)

        ttk.Label(self, text=self.T_Sensor.sensor_name).grid(row=1, column=1)
        ttk.Label(self, textvariable=self.T_var).grid(row=2, column=1)

        self._setVars()

    def _setVars(self):
        prec = 1
        self.mDot_var.set(round(self.mDot_Sensor.value,prec))
        self.T_var.set(round(self.T_Sensor.value,prec))
        self.after(100, self._setVars)

class Frame_Box_Single_Temp(tk.Frame):
    def __init__(self, parent, sensor: PT100):
        super().__init__(master=parent)
        self.sensor = sensor
        self.T_var = tk.DoubleVar()
        self.grid_rowconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure((0,1), weight=1, uniform='a')

        ttk.Label(self, text=sensor.sensor_name).grid(row=0, column=0)
        ttk.Label(self, textvariable=self.T_var).grid(row=0, column=1)

        self._setVars()

    def _setVars(self):
        prec = 1
        self.T_var.set(round(self.sensor.value,prec))
        self.after(100, self._setVars)

class Frame_Box_Temps(tk.Frame):
    def __init__(self, parent, name:str, sensorsList: list[PT100]):
        super().__init__(master = parent, highlightbackground="gray", highlightthickness=1)
        ttk.Label(self,text=name, font=('Arial', 14, 'bold')).pack()
        for i,sensor in enumerate(sensorsList):
            Frame_Box_Single_Temp(parent=self, sensor=sensor).pack()

if __name__ == '__main__':
    # my used device
    labjack = ljm.openS("T7", "USB", "ANY") # labjack T7 Pro

    # my paths
    configPath = Path(__file__).parent.absolute() / 'configs'
    savePath = Path(__file__).parent.absolute() / 'data'

    # my handlers
    config = Configuration(pathToConfigFiles=configPath)
    mdh = MeasurementDataHandler(device=labjack, configuration=config)
    exp_handler = ExperimentHandler(mdh=mdh)
    exp_handler.setPathToSave(pathToSave=savePath)
    
    # GUI
    
    window = tk.Tk()
    window.title('rCFD Experiment')

    window.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a')
    window.grid_columnconfigure((0,1,2), weight=1, uniform='a')

    # header
    header=ttk.Label(window, text='LCM rCFD Experiment', font=('Arial', 30, 'bold'))
    header.grid(row=0, column=0, columnspan=3)


    input1 = Frame_massflow(
        parent=window,
        name='Warm/Cold Input',
        mDot_Sensor=mdh.getSensorByName('warm_massflow'),
        T_Sensor=mdh.getSensorByName('Twarm'))
    input1.grid(row=1, column=0, sticky='nsew')

    input1 = Frame_massflow(
        parent=window,
        name='Cold Input',
        mDot_Sensor=mdh.getSensorByName('cold_massflow'),
        T_Sensor=mdh.getSensorByName('Tcold'))
    input1.grid(row=2, column=0, sticky='nsew')

    sensors = ['h=35mm','h=65mm','h=95mm','h=125mm','h=155mm','h=185mm','h=215mm']
    sensorList = [mdh.getSensorByName(name=s) for s in sensors]
    
    temps = Frame_Box_Temps(
        parent=window,
        name='Box Temperatures',
        sensorsList=sensorList)
    temps.grid(row=1,column=1, rowspan=2)

    aq_control = Frame_aquisitionControl(parent=window, handler=exp_handler)
    aq_control.grid(row=3, column=0, columnspan=3, sticky='nsew')

    window.mainloop()
