import tkinter as tk
from IKA import IKA_Ministar40
from view import GUI
from controller import Controller 

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('IKA Test')

        # create a model
        model = IKA_Ministar40(port = 'COM9', speedLimit=120)

        # create a view and place it on the root window
        view = GUI(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()