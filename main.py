from functions.config import Configuration
from functions.sensors import PT100, Flowmeter, Switch
from functions.periodicHandler import periodicFunctionHandler
from labjack import ljm
import os
from datetime import datetime
import csv
from pathlib import Path


class ExperimentHandler():
    def __init__(self, pathToConfig: Path, measurementDevice: ljm) -> None:
        self.conf = Configuration(pathToConfigFiles=pathToConfig)
        self.mdh = MeasurementDataHandler(device=measurementDevice, configuration=self.conf)

    @property
    def configuration(self):
        pass

    def _measure(self):
        sample = self.mdh.all_sensor_values()
        self.data.append(sample)
        self.mdh.printCMD()

    def start(self,  pathToSave: Path):
        '''starts an experiment'''
        self.pathToSave = pathToSave
        print('Start measurement')
        
        self.data = []
        self.pfh = periodicFunctionHandler(func = self._measure)
        self.pfh.start(sample_rate = self.conf.experiment['SAMPLE_RATE'])


    def stop(self):
        '''stops an experiment'''
        self.pfh.stop()
        os.system('cls')
        print('Stop Measurement')

        print('Save Data')
        self._createDirectory()

        # Save config file
        self.conf.save(pathToSave=self.exp_dir) # save config File
        print('Configuration File saved')

        # save measurement data
        filename = str(self.exp_dir / 'data.csv')
        with open(filename, 'a', newline = '') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(self.mdh.sensor_names) # header
            csvwriter.writerows(self.data) 
        print('Measurement data saved')    

    def _createDirectory(self):
        self.datetime = datetime.now()
        self.dirname = self.datetime.strftime('%Y%m%d_%H%M%S')
        self.dirname += '_LCM'
        self.dirname += '_inlet=' + self.conf.experiment['INLET']
        self.dirname += '_outlet=' + self.conf.experiment['OUTLET']

        self.exp_dir = Path(self.pathToSave, self.dirname)
        self.exp_dir.mkdir(parents=True, exist_ok=True)
        
               
class MeasurementDataHandler():
    def __init__(self, device:ljm, configuration: Configuration) -> None:
        self.device = device
        self.conf = configuration
        self.SENSOR_LIST = []
        def appendSensorCategory(Category: str, sensorClass) -> None:
            for name, ch in self.conf.labjack[Category].items():
                s = sensorClass()
                s.setChannel(device = self.device, sensor_name = name, channel = ch)
                self.SENSOR_LIST.append(s)
        appendSensorCategory('PT100', PT100)
        appendSensorCategory('Flowmeter', Flowmeter)
        appendSensorCategory('Switch', Switch)

        self.sensor_names = [s.sensor_name for s in self.SENSOR_LIST]
        self.sensor_names.insert(0, 'timestamp')

    def printCMD(self) -> str:
        os.system('cls')
        [print(s) for s in self.SENSOR_LIST] 

    def all_sensor_values(self) -> list:
        data = [s.value for s in self.SENSOR_LIST]
        data.insert(0, datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        return data



if __name__ == '__main__':
    import time
    import tkinter as tk
    from tkinter import ttk
    
    device = ljm.openS("T7", "USB", "ANY") # labjack T7 Pro
    configPath = Path(__file__).parent.absolute() / 'configs'
    savePath = Path(__file__).parent.absolute() / 'data'
    exp_handler = ExperimentHandler(measurementDevice = device, pathToConfig = configPath)
    
    
    window = tk.Tk()
    window.title('Test Function')
    sample_rate_var = tk.IntVar(value=1)
    ttk.Button(window, text='Experiment Start', command= lambda: exp_handler.start(savePath)).pack()
    ttk.Button(window, text='Experiment Stop', command=exp_handler.stop).pack()
    window.mainloop()
    



