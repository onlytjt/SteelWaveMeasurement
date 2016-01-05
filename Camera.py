import cv2
import numpy as np
import time
from pymba import *

class CameraInterface:
    def __init__(self):
        self.vimba = 0
        self.camera = 0
        self.cameraIds = 0
        self.frame0 = 0
        self.frame1 = 0
        self.moreUsefulImgData = 0

    def openCamera(self):
        self.vimba = Vimba()
        self.vimba.startup()
        print "The Vimba lib version is:", self.vimba.getVersion()
        print "Vimbai run successfully!"
        system = self.vimba.getSystem()

        # list available cameras (after enabling discovery for GigE cameras)
        system.runFeatureCommand("GeVDiscoveryAllOnce")
        time.sleep(0.2)
        self.cameraIds = self.vimba.getCameraIds()
        print "Available cameras", self.cameraIds
        self.camera = self.vimba.getCamera(self.cameraIds[0])
        self.camera.openCamera()

    def setCameraFeature(self):
        # show camera default features and set some features
        #cameraFeatureNames = camera.getFeatureNames()
        #print cameraFeatureName
        print "CameraFeature: ", self.camera.AcquisitionMode
        self.camera.AcquisitionMode = 'SingleFrame'

        # announce memory for frame
        self.frame0 = self.camera.getFrame()
        self.frame1 = self.camera.getFrame()
        self.frame0.announceFrame()

    def captureFrame(self):
        self.camera.startCapture()
        self.frame0.queueFrameCapture()
        self.camera.runFeatureCommand('AcquisitionStart')
        self.camera.runFeatureCommand('AcquisitionStop')
        self.frame0.waitFrameCapture()

        imgData = self.frame0.getBufferByteData()
        # self.moreUsefulImgData = np.ndarray(buffer = self.frame0.getBufferByteData(),
        #                            dtype = np.uint8,
        #                            shape = (self.frame0.height,
        #                                     self.frame0.width,
        #                                     1))
        self.moreUsefulImgData = np.ndarray(buffer = self.frame0.getBufferByteData(),
                                   dtype = np.uint8,
                                   shape = (self.frame0.height,
                                            self.frame0.width))
        self.camera.endCapture()

    def showImage(self):
        cv2.imshow("Show Image", self.moreUsefulImgData)

    def endShow(self):
        cv2.destroyAllWindows()
        self.vimba.shutdown()

    def closeCamera(self):
        self.vimba.shutdown()



def main():
    ins = CameraInterface()
    ins.openCamera()
    ins.setCameraFeature()
    while True:
        ins.captureFrame()
        ins.showImage()
        if cv2.waitKey(1) == 27: # press esc to quit
            break
    ins.endShow()

if __name__ == "__main__":
    pass

