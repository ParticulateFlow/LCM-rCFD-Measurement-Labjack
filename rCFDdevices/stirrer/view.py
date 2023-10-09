import tkinter as tk
from tkinter import ttk
        
class GUI(tk.Frame):
    def __init__(self, parent):
        self.controller = None

        super().__init__(master=parent, highlightbackground="gray", highlightthickness=1, padx=10,pady=10)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.rowconfigure((3,4), weight=1)
        self.columnconfigure((0,1), weight=1)
        
        # Header
        ttk.Label(self, text='Stirrer Control', font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2)

        # left colum - slider
        self.scale = ttk.Scale(self,
                               from_= 30, to=120, value=60, 
                               command=lambda event: self.label.config(text=f"{int(self.scale.get())} U/min") ,
                               orient='vertical', length=150)
        self.scale.bind("<ButtonRelease-1>",lambda event: self.update() )
        self.scale.grid(row=1, column=0, padx=20, pady=20)
        self.label = ttk.Label(self, text=f"{int(self.scale.get())} U/min")
        self.label.grid(row=2, column=0)

        # second column - buttons
        self.control = tk.Frame(self)
        ttk.Button(self.control, text='Start', command=self.start). pack()
        ttk.Button(self.control, text='Stop', command=self.stop).pack()
        #ttk.Button(self.control, text='Reset Stirrer', command=self.stirrer.reset).pack()
        #ttk.Button(self.control, text='Read RPM', command=self.stirrer.readRPM).pack()
        self.control.grid(row=1, column=1, columnspan=2)

        # current rpm
        # self.soll_rpm = tk.IntVar()
        # ttk.Label(self, text='Current RPM:', font=('Arial', 10)).grid(row=3,column=0, columnspan=2)
        # ttk.Label(self, textvariable=self.soll_rpm,  font=('Arial', 10, 'bold')).grid(row=4,column=0, columnspan=2)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
        self.update()

    def update(self):
        if self.controller:
            self.controller.update(rpm = int(self.scale.get()))
    
    def start(self):
        if self.controller:
            self.controller.start(rpm = int(self.scale.get()))
    
    def stop(self):
        if self.controller:
            self.controller.stop()
        


    # def _update(self):
    #     val = self.stirrer.currentSpeed
    #     self.soll_rpm.set(val)
    #     self.after(1000,self._update)

