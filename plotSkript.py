import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from pathlib import Path
from tkinter import Tk

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import seaborn as sns
from datetime import datetime
from functions.config import Configuration

sns.set()

class Visualisation():
    def __init__(self, start_dir) -> None:
        # Directory
        
        window = tk.Tk()
        window.wm_attributes('-topmost', 1)
        # Here, window.wm_attributes('-topmost', 1) and "parent=window" argument help open the dialog box on top of other windows
        window.withdraw()   # this supress the tk window

        self.directory = Path(filedialog.askdirectory(initialdir=start_dir))

        self.savePath = self.directory / 'plots'
        self.savePath.mkdir(exist_ok=True)

        # Config
        self.conf = Configuration(pathToConfigFiles=self.directory)

        # Dataframe
        self.df = pd.read_csv(str(self.directory/'data.csv'))
        self.df['ts'] = self.df['timestamp'].apply(lambda s: pd.Timestamp(datetime.strptime(s,'%Y%m%d_%H%M%S_%f')))
        self.df['ts'] -= self.df['ts'].iat[0]
        self.df['time'] = self.df['ts']/pd.Timedelta(1, 's')
        self.df['sum_massflow'] = self.df['warm_massflow'] + self.df['cold_massflow']

    def plot_all_single(self):
        self._plotSingle(self._massflow, 'massflow.png')
        self._plotSingle(self._systemTemps, 'system_temps.png')
        self._plotSingle(self._boxTemps, 'box_temps.png')
        
    def plot_Overview(self):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(14, 10))
        fig.tight_layout(pad=3.0)
        self._massflow(ax[0])
        self._systemTemps(ax[1])
        self._boxTemps(ax[2])
        fig.savefig(str(self.directory / 'overview.png'))

    
    def _plotSingle(self, plot_func: callable, filename: str) -> None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
        fig.tight_layout(pad=3.0)
        plot_func(ax=ax)
        fig.savefig(str(self.savePath / filename))

    def _massflow(self, ax):
        self.df.plot(x='time', y=['warm_massflow','cold_massflow'], ax=ax,
            color = ['red', 'blue'],
            lw=1, grid=True, title="Massflow",
            xlabel="Seconds", ylabel="ml/s")
        
        self.df.plot(x='time', y='sum_massflow', ax=ax,
            color = 'black',
            lw=2, grid=True, title="Massflow",
            xlabel="Seconds", ylabel="ml/s")

    def _systemTemps(self, ax):
        # plot sensors temp
        self.df.plot(x='time', y=['Twarm','Tcold','Tout'], ax=ax,
            color = ['red','blue','black'],
            lw=2, grid=True, title="System",
            xlabel="Seconds", ylabel=f"{chr(176)}C")
        # ax.axhline(y=conf.experiment['THERMOSTAT'], color='r', linestyle='--')
        
    def _boxTemps(self, ax):
        self.df.plot(x='time', y=['h=215mm','h=185mm','h=155mm','h=125mm','h=95mm','h=65mm','h=35mm'], ax=ax,
            lw=1, grid=True, title="Box",
            xlabel="Seconds", ylabel=f"{chr(176)}C")

        

if __name__ == '__main__':
    start_dir = Path("X:\LCM-Demonstrator\Michael\themes\4_experiments\0_Labjack_Ring_System")
    vis = Visualisation(start_dir=start_dir)
    vis.plot_all_single()
    vis.plot_Overview()

print("Skript finished")