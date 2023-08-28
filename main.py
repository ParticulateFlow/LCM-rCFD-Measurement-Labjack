import tkinter as tk
from tkinter import ttk

from functions.config import Configuration
from functions.measurementHandler import MeasurementDataHandler
from functions.experimentHandler import ExperimentHandler
from functions.frames import Frame_DataOverview, Frame_aquisitionControl
from functions.stirrer import IKA_Ministar40

from labjack import ljm
from pathlib import Path
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class Frame_timeplot(tk.Frame):
    def __init__(self, parent, edh: ExperimentHandler):
        super().__init__(master=parent)
        self.edh = edh
        self.label = ttk.Label(self)
        self.label.pack()
        self.canvas = None
        self._update()
        

    def _update(self):
        if not self.edh.is_running:
            self.label.config(text='Not running')
            if self.canvas:
                self.canvas.grid_forget()
                self.canvas = None
        elif len(self.edh.data) > 0:  
            self.fig = plt.Figure(figsize=(10,6), dpi=100) 
            df = pd.DataFrame(self.edh.data, columns=self.edh.mdh.sensor_names)
            ax = self.fig.add_subplot(111)
            df.plot(x='timestamp',
                    y=['Twarm','Tcold','Tout'],
                    color = ['red','blue','black'],
                    linewidth = 2,
                    ax=ax)
            df.plot(x='timestamp',
                    y=['h=35mm','h=65mm','h=95mm','h=125mm','h=155mm','h=185mm','h=215mm'],
                    linewidth = 1,
                    ax=ax)
            thermoStat  = self.edh.mdh.thermostat
            ax.axhline(thermoStat, color ='black', lw = 4, ls='dashed')
            ax.set_ylim([15,thermoStat  + 20])
            ax.xaxis.set_visible(False)
            ax.set_ylabel(f'Temperature [{chr(176)}C]')
            ax.grid()
            self.fig.tight_layout()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.label).get_tk_widget()
            self.canvas.grid(row=0, column=0)
            
                   

        self.after(1000, self._update)    


if __name__ == '__main__':
    # my used device
    labjack = ljm.openS("T7", "USB", "ANY") # labjack T7 Pro
    ministar40 = IKA_Ministar40(usbName = 'USB', speedLimit=120)

    # my paths
    configPath = Path(__file__).parent.absolute() / 'configs'
    savePath = Path(__file__).parent.absolute() / 'data'

    # my handlers
    config = Configuration(pathToConfigFiles=configPath)
    mdh = MeasurementDataHandler(device=labjack,stirrer=ministar40, configuration=config)
    exp_handler = ExperimentHandler(mdh=mdh)
    exp_handler.setPathToSave(pathToSave=savePath)
    
    
    # GUI
    window = tk.Tk()
    window.title('rCFD Experiment')

    # header
    ttk.Label(master=window, text='LCM rCFD Experiment', font=('Arial', 30, 'bold')).pack()
    # notebook
    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, expand=True)


    frame_overview = Frame_DataOverview(parent=window, mdh=mdh)
    frame_overview.pack()

    frame_time = Frame_timeplot(parent=window, edh=exp_handler)
    frame_time.pack()

    notebook.add(frame_overview, text='Overview')
    notebook.add(frame_time, text='Timeplot')

    # Control
    Frame_aquisitionControl(parent=window, handler=exp_handler).pack()
    window.mainloop()
