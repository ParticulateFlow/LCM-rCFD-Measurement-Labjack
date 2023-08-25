import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk

# IN_NAME Gerätenamen lesen
# IN_PV_3 Pt1000 Wert lesen
# IN_PV_4 aktuellen Drehzahlwert lesen
# IN_PV_5 aktuellen Drehmomentwert lesen
# IN_SP_4 Nenndrehzahlwert lesen
# IN_SP_5 Wert der Drehmomentbegrenzung lesen
# IN_SP_6 Wert der Drehzahlbegrenzung lesen
# IN_SP_8 Wert der Sicherheitsdrehzahl lesen
# OUT_SP_4 Nenndrehzahlwert einstellen
# OUT_SP_5 Wert der Drehmomentbegrenzung einstellen
# OUT_SP_6 Wert der Drehzahlbegrenzung einstellen
# OUT_SP_8 Wert der Sicherheitsdrehzahl einstellen
# START_4 Motor starten
# STOP_4 Motor stoppen
# RESET auf Normalbetrieb umschalten
# OUT_MODE_n 
# (n= 1 or 2) Drehrichtung einstellen
# IN_MODE Drehrichtung lese

class IKA_ministar40():
    '''Control class for the IKA ministar 40'''
    def __init__(self, maxRpm: int) -> None:
        self.maxRpm = maxRpm
        self.rpm = 30

        # Find right port
        ports = serial.tools.list_ports.comports() #all available Ports
        nameList = [ports[i].description for i in range(len(ports))]
        print(nameList)
        try:
            index = [idx for idx, s in enumerate(nameList) if 'USB Serial Device' in s][0]
        except:
            raise ConnectionError("Device not connected")

        print(f"Device found: Try to open {ports[index].name}:{ports[index].description}")

        # Init serial connection
        self.ser = serial.Serial()
        self.ser.baudrate = '9600'
        self.ser.port = ports[index].name
        self.ser.open()
        print("Stirrer sucessfully connected")

        self.reset()

    def setRPM(self, rpm: int):
        '''sets the rpm'''
        self.rpm = rpm
        if self.rpm < 0: ValueError('Only positive numbers allowed')
        if self.rpm > self.maxRpm: raise ValueError('Maxiumum rpm ') #("Number of reovultion > than maximum")
        out_string = f"OUT_SP_4 {self.rpm} \r\n"
        self.ser.write(bytes(out_string, 'utf-8'))

    def reset(self) -> None:
        '''resets the stirrer'''
        self.ser.write(bytes("RESET \r\n",'utf-8'))

    # def readRPM(self):
    #     self.ser.write("IN_PV_4 \r\n")
    #     rpm = self.ser.readline()
    #     print(rpm)

    def start(self) -> None:
        '''Starts the stirrer'''
        self.ser.write(bytes("START_4 \r\n", 'utf-8'))
        self.setRPM(self.rpm)
        print('Start Stirrer')
                
    def stop(self) -> None:
        '''Stops the stirrer'''
        self.ser.write(bytes("STOP_4 \r\n", 'utf-8'))
        self.setRPM(0)
        print('Stop Stirrer')
        
        
class Frame_Stirrer(tk.Frame):
    def __init__(self, parent, stirrer: IKA_ministar40):
        super().__init__(master=parent)
        self.stirrer = stirrer

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.columnconfigure((0,1), weight=1)
        
        # first column
        ttk.Label(self, text='Stirrer Control', font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2)
        self.scale = ttk.Scale(self,
                               from_=0, to=self.stirrer.maxRpm, 
                               value=30, command=lambda event: self._updateScale(), 
                               orient='vertical', length=150)
        self.scale.grid(row=1, column=0, padx=20, pady=20)
        self.label = ttk.Label(self)
        self.label.grid(row=2, column=0)

        # second column
        self.control = tk.Frame(self)
        ttk.Button(self.control, text='Start', command=self.stirrer.start). pack()
        ttk.Button(self.control, text='Stop', command=self.stirrer.stop).pack()
        ttk.Button(self.control, text='Reset Stirrer', command=self.stirrer.reset).pack()
        #ttk.Button(self.control, text='Read RPM', command=self.stirrer.readRPM).pack()
        self.control.grid(row=1, column=1, columnspan=2)

        self._updateScale()

    def _updateScale(self):
        self.rpm = int(self.scale.get())
        self.stirrer.setRPM(rpm=self.rpm)
        self.label.config(text=f"{self.rpm} U/min")

if __name__ == "__main__":
    IKA_ministar40 = IKA_ministar40(maxRpm=120)
    window = tk.Tk()
    window.title('rCFD Experiment')
    Frame_Stirrer(window, stirrer=IKA_ministar40).pack()
    window.mainloop()


