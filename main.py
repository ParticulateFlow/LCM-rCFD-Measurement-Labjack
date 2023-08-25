import tkinter as tk
from tkinter import ttk

from functions.config import Configuration
from functions.measurementHandler import MeasurementDataHandler
from functions.experimentHandler import ExperimentHandler
from functions.frames import Frame_DataOverview, Frame_aquisitionControl

from labjack import ljm
from pathlib import Path


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

    # header
    ttk.Label(master=window, text='LCM rCFD Experiment', font=('Arial', 30, 'bold')).pack()
    # notebook
    notebook = ttk.Notebook(window)
    notebook.pack(pady=10, expand=True)


    frame_overview = Frame_DataOverview(parent=window, mdh=mdh)
    frame_overview.pack()
    frame_blank = ttk.Frame(window)
    frame_blank.pack()

    notebook.add(frame_overview, text='Overview')
    notebook.add(frame_blank, text='Timeplot')

    # Control
    Frame_aquisitionControl(parent=window, handler=exp_handler).pack()
    window.mainloop()
