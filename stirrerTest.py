import tkinter as tk
from tkinter import ttk
from stirrer import IKA_Ministar40
        
class Frame_Stirrer(tk.Frame):
    def __init__(self, parent, stirrer: IKA_Ministar40):
        super().__init__(master=parent, highlightbackground="gray", highlightthickness=1, padx=10,pady=10)
        self.stirrer = stirrer

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.rowconfigure((3,4), weight=1)
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

        # current rpm
        self.soll_rpm = tk.IntVar()
        ttk.Label(self, text='Current RPM:', font=('Arial', 10)).grid(row=3,column=0, columnspan=2)
        ttk.Label(self, textvariable=self.soll_rpm,  font=('Arial', 10, 'bold')).grid(row=4,column=0, columnspan=2)
        self._update()
    
    def start(self):
        val = int(self.scale.get())
        self.stirrer.start()
        self.stirrer.set_ratedSpeed(val)

    def _update(self):
        val = self.stirrer.currentSpeed
        self.soll_rpm.set(val)
        self.after(1000,self._update)

if __name__ == "__main__":
    stirrer = IKA_Ministar40(usbName = 'USB', speedLimit=120)
    window = tk.Tk()
    window.title('rCFD Experiment')
    Frame_Stirrer(window, stirrer=stirrer).pack()
    window.mainloop()