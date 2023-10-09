class Controller:
    def __init__(self, stirrer, view):
        self.stirrer = stirrer
        self.view = view

    def start(self, rpm: int):
        """
        Starts the stirrer
        with a given rpm 
        """

        try:
            self.stirrer.start()
            self.stirrer.set_ratedSpeed(rpm)
        except:
            pass
    
    def stop(self):
        """
        Stops the stirrer
        """

        try:
            self.stirrer.stop()
        except:
            pass

    def update(self, rpm: int):
        try:
            self.stirrer.set_ratedSpeed(rpm)
        except:
            pass