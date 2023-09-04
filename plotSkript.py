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

        # Config
        self.conf = Configuration(pathToConfigFiles=self.directory)

        # Dataframe
        self.df = pd.read_csv(str(self.directory/'data.csv'))
        self.df['ts'] = self.df['timestamp'].apply(lambda s: pd.Timestamp(datetime.strptime(s,'%Y%m%d_%H%M%S_%f')))
        self.df['ts'] -= self.df['ts'].iat[0]
        self.df['time'] = self.df['ts']/pd.Timedelta(1, 's')
        self.df['sum_massflow'] = self.df['warm_massflow'] + self.df['cold_massflow']

    def plot_all_single(self):
        self.savePath = self.directory / 'plots_single'
        self.savePath.mkdir(exist_ok=True)
        self._plotSingle(self._massflow, 'massflow.png')
        self._plotSingle(self._systemTemps, 'system_temps.png')
        self._plotSingle(self._tankTemps, 'tank_temps.png')
        self._plotSingle(self._stirrerRPM, 'stirrer.png')
        self._plotSingle(self._switch, 'switch.png')
        
    def plot_Overview(self):
        fig, ax = plt.subplots(nrows=5, ncols=1, figsize=(14, 10))
        fig.tight_layout(pad=3.0)
        self._massflow(ax[0])
        ax[0].get_xaxis().set_visible(False)
        self._systemTemps(ax[1])
        ax[1].get_xaxis().set_visible(False)
        self._tankTemps(ax[2])
        ax[2].get_xaxis().set_visible(False)
        self._stirrerRPM(ax[3])
        ax[3].get_xaxis().set_visible(False)
        self._switch(ax[4])
        fig.savefig(str(self.directory / 'overview.png'))

    def plot_Temps_withStirrer(self):
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(14, 10))
        ax[0].get_xaxis().set_visible(False)
        fig.tight_layout(pad=3.0)
        self._systemTemps(ax[0])
        self._tankTemps(ax[0])
        self._stirrerRPM(ax[1])
        fig.savefig(str(self.directory / 'temps_with_stirrer.png'))

    def plot_Temps_stirrer_highlighted(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
        fig.tight_layout(pad=3.0)
        self._systemTemps(ax)
        self._tankTemps(ax)

        y1, y2 = ax.get_ylim()
        ax.fill_between(self.df['time'], y1, y2, where=self.df["stirrer"] > 0, color='darkgray', alpha=0.5,interpolate=True)
        ax.set_ylim([y1,y2])

        # y1, y2 = ax.get_ylim()
        # ax.fill_between(self.df['time'], y1, y2, where=self.df["switch"] > 0, color='red', alpha=0.1,interpolate=True)
        # ax.set_ylim([y1,y2])
        # Determine when the RecordType Changes
        periods = self.df[self.df['switch'].diff()!=0].index.values
        for item in periods[1::]:
            plt.axvline(item, ymin=0, ymax=1, color='green',ls='--', lw=6)


        fig.savefig(str(self.directory / 'temps_stirrer_highlighted.png'))

    
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
        ax.title.set_size(20)

    def _systemTemps(self, ax):
        # plot sensors temp
        self.df.plot(x='time', y=['Twarm','Tcold','Tout'], ax=ax,
            color = ['red','blue','black'],
            lw=2, grid=True, title="System",
            xlabel="Seconds", ylabel=f"{chr(176)}C")
        ax.title.set_size(20)
        # ax.axhline(y=conf.experiment['THERMOSTAT'], color='r', linestyle='--')
        
    def _tankTemps(self, ax):
        self.df.plot(x='time', y=['h=215mm','h=185mm','h=155mm','h=125mm','h=95mm','h=65mm','h=35mm'], ax=ax,
            lw=1, grid=True, title="Stirred Tank",
            xlabel="Seconds", ylabel=f"{chr(176)}C")
        ax.title.set_size(20)
        
    def _stirrerRPM(self,ax):
        self.df.plot(x='time', y='stirrer', ax=ax,
            lw=1, grid=True, title="Stirrer",
            xlabel="Seconds", ylabel="U/min")
        ax.title.set_size(20)

    def _switch(self,ax):
        self.df['switch'] = self.df['warm/cold'].map({'warm': 1, 'cold': 0}) 
        self.df.plot(x='time', y='switch', ax=ax,
            lw=1, grid=True, title="Bypass",
            xlabel="Seconds", ylabel="cold/warm")
        ax.title.set_size(20)


        

if __name__ == '__main__':
    start_dir = Path("X:\LCM-Demonstrator\Michael\themes\4_experiments\0_Labjack_Ring_System")
    vis = Visualisation(start_dir=start_dir)
    vis.plot_all_single()
    vis.plot_Overview()
    vis.plot_Temps_withStirrer()
    vis.plot_Temps_stirrer_highlighted()

print("Skript finished")