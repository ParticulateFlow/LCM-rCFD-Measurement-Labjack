from time import sleep
import threading

class periodicFunctionHandler():
    '''Class for handling periodic tasks like the saving of my data'''
    def __init__(self, func: callable) -> None:
        self.func = func
        self.event = threading.Event()   
        self.thread = threading.Thread(target=self._background_task, daemon=True)
        self.thread.start()
    
    def setCallable(self, func: callable):
        '''setter for the callable function'''
        self. func = func

    def start(self, sample_rate: int):
        '''starts the callable function with a specific sample rate'''
        self.time = 1 / sample_rate
        self.event.set()

    def stop(self):
        '''stops the callable function'''
        self.event.clear()

    def _background_task(self):
        '''private background task'''
        while True:
            self.event.wait()
            sleep(self.time)
            if self.event.is_set():
                self.func()
         

if __name__ == '__main__':
    import tkinter as tk
    from tkinter import ttk
    import datetime

    t = periodicFunctionHandler(lambda: print(datetime.datetime.now()))  
    window = tk.Tk()
    window.title('Test Function')
    sample_rate_var = tk.IntVar(value=1)
    bStart = ttk.Button(window, text='Start', command=lambda: t.start(sample_rate_var.get()))
    bStop = ttk.Button(window, text='Stop', command=t.stop)
    input = ttk.Entry(window, textvariable=sample_rate_var)
    bStart.pack()
    bStop.pack()
    input.pack()
    window.mainloop()