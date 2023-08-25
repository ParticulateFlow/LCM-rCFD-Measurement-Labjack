from pathlib import Path
import csv
import os
from measurementHandler import MeasurementDataHandler
from periodicHandler import periodicFunctionHandler


class ExperimentHandler():
    def __init__(self, mdh: MeasurementDataHandler) -> None:
        self.mdh = mdh

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
        self.pfh.start(sample_rate = self.mdh.sample_rate)


    def stop(self):
        '''stops an experiment'''
        self.pfh.stop(), os.system('cls')
        print('Stop Measurement')

        print('Save Data')
        self._createDirectory()
        self.mdh.conf.saveConfiguration(pathToSave=self.exp_dir) # save config File
        print('Configuration File saved')
        filename = str(self.exp_dir / 'data.csv')
        with open(filename, 'a', newline = '') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(self.mdh.sensor_names) # header
            csvwriter.writerows(self.data) 
        print('Measurement data saved')    

    def _createDirectory(self):
        self.dirname = self.mdh.timestamp.strftime('%Y%m%d_%H%M%S')
        self.dirname += '_LCM_inlet=' + self.mdh.inlet_conf + '_outlet=' + self.mdh.outlet_conf

        self.exp_dir = Path(self.pathToSave, self.dirname)
        self.exp_dir.mkdir(parents=True, exist_ok=True)
        

if __name__ == '__main__':
    import time
    import tkinter as tk
    from tkinter import ttk
    from config import Configuration
    from labjack import ljm
    

    # my used device
    labjack = ljm.openS("T7", "USB", "ANY") # labjack T7 Pro

    # my paths
    configPath = Path(__file__).parent.parent.absolute() / 'configs'
    savePath = Path(__file__).parent.parent.absolute() / 'data'

    config = Configuration(pathToConfigFiles=configPath)
    exp_handler = ExperimentHandler(mdh=MeasurementDataHandler(device=labjack, configuration=config))
    
    
    window = tk.Tk()
    window.title('Test experimentHandler')
    ttk.Button(window, text='Experiment Start', command= lambda: exp_handler.start(savePath)).pack()
    ttk.Button(window, text='Experiment Stop', command=exp_handler.stop).pack()
    window.mainloop()
    



