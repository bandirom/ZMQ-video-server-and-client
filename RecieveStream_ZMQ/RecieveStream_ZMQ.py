import cv2
#import face_recognition
import base64
import zmq
import socket as s
import threading
import numpy as np
from datetime import timedelta, datetime
import logging
import argparse

MyIp = s.gethostbyname(s.gethostname())
parser = argparse.ArgumentParser(description='ZMQ video client. Only for Python 3.6 and higher')
parser.add_argument('-ip', '--IP', 
                    type = str, 
                    default = MyIp, 
                    help = f'IP where will be using ZMQ video client. (default = {MyIp} - your IP-adress for test on One PC)')
parser.add_argument('-p','--port', type=int, default = 5000, help='Port where will be using ZMQ video client (default = 5000)')
Namespace = parser.parse_args()


logFormatter = '(%(threadName)-10s) - %(levelname)s - %(asctime)s - %(message)s'
logging.basicConfig(format = logFormatter, level = logging.INFO)
logger = logging.getLogger(__name__)

class Network(threading.Thread):
    def __init__(self):      
        logger.debug('Running recieve client')
        self.MyIp = Namespace.IP # 192.168.1.102
        self.Port = Namespace.port
        self.initZMQ()
        logger.info('Successfull initialization')
        logger.info(f'Ip-adress: {self.MyIp}:{self.Port}')
        threading.Thread.__init__(self, target = self.RecieveStream)
        self.start()


    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.bind("tcp://" + self.MyIp + ":" + str(self.Port))

    def RecieveStream(self):
        logger.debug('Start second thread')
        while True:
            jpg_as_text = self.socket.recv()
            openCV.DecodeBase64ToFrame(jpg_as_text)

class Open_Cv():
    def __init__(self):      
        self.now = datetime.now()
        self.Init_CurrentTimeOnFrame()
        self.Init_CurrentFpsOnFrame()

    def Init_CurrentTimeOnFrame(self):
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.place_1 = (12,30)
        self.fontScale = 1
        self.fontColor = (255,255,255)
        self.lineType = 1

    def Init_CurrentFpsOnFrame(self):
        self.place_2 = (300,30)
        self.MiliSeconds = 1000
        self.FPS = 0
        self.save_fps = 0

    def DecodeBase64ToFrame(self, jpg_as_text):
        self.Display(self.readb64(jpg_as_text))

    def readb64(self,uri):
        uri = base64.b64decode(uri)
        nparr = np.frombuffer(uri,np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img

    def InsertTextOnFrame(self, frame):
        self.CurrentTime = datetime.now()
        cv2.putText(frame, self.CurrentTime.strftime('%H:%M:%S %Y.%m.%d'),
                self.place_1,self.font,self.fontScale,self.fontColor, self.lineType)
        if self.CurrentTime - self.now >= timedelta(milliseconds=self.MiliSeconds):
            self.save_fps = str(self.FPS)
            self.now = self.CurrentTime
            self.FPS = 0
        else:
            self.FPS += 1
        cv2.putText(frame, "FPS: " + str(self.save_fps),
                self.place_2,self.font,self.fontScale,self.fontColor, self.lineType)


    def Display(self, frame):
        self.InsertTextOnFrame(frame)
        cv2.imshow('Recieve Frame', frame)  # Display the resulting image
        if cv2.waitKey(1) & 0xFF == ord('q'): # Hit 'q' on the keyboard to quit!
            cv2.destroyAllWindows()
             

if __name__=='__main__':
    openCV = Open_Cv()
    n = Network()