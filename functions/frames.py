import tkinter as tk
from tkinter import ttk

from .measurementHandler import MeasurementDataHandler
from .experimentHandler import ExperimentHandler
from .sensors import PT100, Flowmeter, Switch
from .stirrer import Frame_Stirrer

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
        self.mDot_sensor = mDot_Sensor
        self.T_sensor = T_Sensor

        ttk.Label(self,text=name, font=('Arial', 14, 'bold')).pack()
        self.label1 = ttk.Label(self)
        self.label2 = ttk.Label(self)

        self.label1.pack()
        self.label2.pack()

        self._setVars()

    def _setVars(self):
        self.label1.config(text=str(self.mDot_sensor))
        self.label2.config(text=str(self.T_sensor))

        self.after(1000, self._setVars)

class Frame_Box_Temps(tk.Frame):
    def __init__(self, parent, name:str, sensorsList: list[PT100]):
        super().__init__(master = parent, highlightbackground="gray", highlightthickness=1)
        self.sensorList = sensorsList[::-1]
        self.labelList = []
        ttk.Label(self,text=name, font=('Arial', 14, 'bold')).pack()
        for _ in range(len(self.sensorList)):
            t = ttk.Label(self)
            t.pack(pady=5)
            self.labelList.append(t)
        self._setVars()

    def _setVars(self):
        for label,sens in zip(self.labelList, self.sensorList):
            label.config(text=str(sens))
        self.after(1000, self._setVars)

class Frame_Switch(tk.Frame):
    def __init__(self, parent, name,  switch: Switch):
        super().__init__(master=parent, highlightbackground="gray", highlightthickness=1)
        self.switch = switch
        self.mode = tk.StringVar()

        ttk.Label(self, text=name, font=('Arial', 14, 'bold')).pack()
        ttk.Label(self, textvariable=self.mode).pack()
        self._setVar()
    
    def _setVar(self):
        if self.switch.value == 'warm':
            self.config(bg='red')
        if self.switch.value == 'cold':
            self.config(bg='blue')
        self.mode.set(self.switch.value)
        self.after(1000, self._setVar)

class Frame_Tout(tk.Frame):
    def __init__(self, parent, name, sensor: PT100):
        super().__init__(master=parent, highlightbackground="gray", highlightthickness=1)
        self.sensor = sensor
    
        ttk.Label(self, text=name,font=('Arial', 14, 'bold')).pack()
        self.label = ttk.Label(self, text=str(sensor))
        self.label.pack()
        self._setVar()
    
    def _setVar(self):
        self.label.config(text=str(self.sensor))
        self.after(1000, self._setVar)


class Frame_DataOverview(tk.Frame):
    def __init__(self, parent, mdh: MeasurementDataHandler):
        super().__init__(master=parent)

        self.grid_rowconfigure((0,1,2), weight=1, uniform='a')
        self.grid_columnconfigure((0,1,2), weight=1, uniform='a')

        # first column
        mDot_Sensor = mdh.getSensorByName('warm_massflow')
        T_Sensor = mdh.getSensorByName('Twarm')
        frame_warm = Frame_massflow(self, 'Warm or Cold Water', mDot_Sensor, T_Sensor)

        switch_Sensor = mdh.getSensorByName('warm/cold')
        frame_switch = Frame_Switch(self, 'MODE:', switch=switch_Sensor)

        mDot_Sensor = mdh.getSensorByName('cold_massflow')
        T_Sensor = mdh.getSensorByName('Tcold')
        frame_cold = Frame_massflow(self, 'Cold Water', mDot_Sensor, T_Sensor)

        sensors = ['h=35mm','h=65mm','h=95mm','h=125mm','h=155mm','h=185mm','h=215mm']
        sensorList = [mdh.getSensorByName(name=s) for s in sensors]
        frame_Box = Frame_Box_Temps(self, 'Box Temperatures', sensorList)

        T_Sensor = mdh.getSensorByName('Tout')
        frame_out = Frame_Tout(self, 'Output', T_Sensor)

        frame_stirrer = Frame_Stirrer(parent=self, stirrer=mdh.stirrer)

        #layout
        frame_warm.grid(row=0, column=0, sticky='nsew')
        frame_switch.grid(row=1, column=0, sticky='nsew')
        frame_cold.grid(row=2, column=0, sticky='nsew')
        frame_Box.grid(row=0, column=1, rowspan=3, sticky='nsew')
        frame_out.grid(row=0, column=2, sticky='nsew')
        frame_stirrer.grid(row=1, column=2, rowspan=2, sticky='nsew')