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
mdh = MeasurementDataHandler(device=labjack, configuration=config)

exp_handler = ExperimentHandler(mdh=mdh)


window = tk.Tk()
window.title('Test Function')
sample_rate_var = tk.IntVar(value=1)
ttk.Button(window, text='Experiment Start', command= lambda: exp_handler.start(savePath)).pack()
ttk.Button(window, text='Experiment Stop', command=exp_handler.stop).pack()
window.mainloop()







if __name__ == '__main__':
    
    



