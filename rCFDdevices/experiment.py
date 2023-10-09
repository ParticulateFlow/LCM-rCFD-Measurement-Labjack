from . import ADC, labjackConfiguration
from . import IKA_Ministar40
from . import VideoCamera
import cv2

class rCFD_Experiment():
    def __init__(self) -> None:
        print(f"{'rCFD Experiment':-^40}")
        print("Start init devices")
        
        # Labjack ADC
        self.adc = ADC(ljmConf=labjackConfiguration(device='T7',connection='ETHERNET',identifier='ANY'))

        # IKA Stirrer
        self.stirrer = IKA_Ministar40(port = 'COM9', speedLimit=120)
        self.stirrerState = 'OFF'
        self.stirrerRPM = 0

        # Camera
        self.camera = VideoCamera()

        self.header = list(self.data.keys())

    def stirrer_start(self, rpm: int) -> None:
        self.stirrer.start()
        self.stirrer.set_ratedSpeed(rpm)
        self.stirrerRPM = rpm
        self.stirrerState = 'ON'

    def stirrer_stop(self) -> None:
        self.stirrer.stop()
        self.stirrerState = 'OFF'

    def stirrer_update(self, rpm: int) -> None:
        self.stirrerRPM = rpm
        self.stirrer.set_ratedSpeed(rpm)

    def saveFrame(self, filename: str):
        bgr = self.camera.frame()
        cv2.imwrite(filename=filename, img=bgr)

    @property
    def data(self):
        d = self.adc.data
        d["stirrerStatus"] = self.stirrerState
        if self.stirrerState == 'ON':
            d["stirrerRPM"] = self.stirrerRPM
        else:
            d["stirrerRPM"] = 0

        return d

if __name__ == '__main__':
    rCFD = rCFD_Experiment()
    print(rCFD.data)
    print(rCFD.header)