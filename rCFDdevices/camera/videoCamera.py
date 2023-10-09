import cv2

class VideoCamera(object):
    def __init__(self):
        port = 0
        self.cap = cv2.VideoCapture(port)

        if self.cap.isOpened():
            # camera working      
            print(f"+ Video Camera on port {port}")

    def __del__(self):
        self.cap.release()

    @property
    def dim(self) -> tuple:
        width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (height, width)       

    def frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        
        
if __name__ == '__main__':
    cap = VideoCamera()
    print(cap.dim)
    cap.saveFrame(filename="test.jpg")