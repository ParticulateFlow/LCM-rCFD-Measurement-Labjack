from pypylon import pylon
import cv2
from threading import Thread

class BaslerCamera():
    '''Class for representing a camera''' 

    def __init__(self) -> None:
        '''inits the camera object'''
        
        # conecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        self.converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


        # reference to the thread for reading next available frame from input stream 
        self.frame = None
        self.newFrame = None
        self.cameraThread = Thread(target=self.cameraThreadFcn, args=())
        self.cameraThread.daemon = True # daemon threads keep running in the background while the program is executing 
        self.cameraThread.start()

    def cameraThreadFcn(self):
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                # Access the image data
                image = self.converter.Convert(grabResult)
                self.newFrame = True
                self.frame = image.GetArray() # BGR image
            grabResult.Release()
               
    def __exit__(self):
        self.camera.StopGrabbing()

if __name__ == '__main__':
    import time

    b = BaslerCamera()
    start_time = time.perf_counter()
    while True:
        if b.newFrame:
            b.newFrame = False
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"FPS = {1/elapsed_time}")
            print(b.frame.shape)
            start_time = time.perf_counter()





