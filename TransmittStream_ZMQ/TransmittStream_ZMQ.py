import cv2
#import face_recognition
import base64
import zmq
import socket as s
import logging
import argparse

MyIp = s.gethostbyname(s.gethostname())
parser = argparse.ArgumentParser(description='ZMQ video server. Please, connect the camera. Only for Python 3.6 and higher')
parser.add_argument('-ip', '--IP', 
                    type=str, 
                    default =MyIp, 
                    help=f'IP where will be using ZMQ video client. (default = {MyIp} - your IP-adress for test on One PC)')
parser.add_argument('-p','--port', 
                    type=int, 
                    default = 5000, 
                    help='Port where will be using ZMQ video client (default = 5000)')
parser.add_argument('-o','--MyPort', 
                    type=int, 
                    default = 5001, 
                    help='Bind your free port (default = 5001)')
parser.add_argument('-i','--CamNumber', 
                    type=int, 
                    default = 0, 
                    help='Your camera index. If two and more camera  (default = 0)')

Namespace = parser.parse_args()

logFormatter = '(%(threadName)-10s) - %(levelname)s - %(asctime)s - %(message)s'
logging.basicConfig(format = logFormatter, level = logging.INFO)
logger = logging.getLogger(__name__)

class Network():
    def __init__(self):    
        logger.debug('Running network connection')
        self.MyIp = MyIp
        self.Port = Namespace.MyPort
        self.ConnectIp = Namespace.IP
        self.ConnectPort = Namespace.port
        if self.initSocket():
            self.Status = True
            logger.info('Successfull initialization')
            logger.info(f'Ip-adress: {self.MyIp}:{self.Port}')
        else:
            self.Status = False

    def initSocket(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        try:
            self.socket.bind(f'tcp://{self.MyIp}:{self.Port}')
            self.socket.connect(f'tcp://{self.ConnectIp}:{self.ConnectPort}')
            return True
        except:
            logger.exception('Socket bind exception')
            return False

    def stream(self, buffer):
        self.socket.send(buffer)


class Open_Cv():
    def __init__(self):
        logger.debug('Running OpenCv and init the camera')
        self.video_capture = cv2.VideoCapture(Namespace.CamNumber)
        self.face_locations = []
        self.ReadCameraLoop()

    def face_recognition(self):
          rgb_frame = frame[:, :, ::-1] # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
          self.face_locations = face_recognition.face_locations(rgb_frame)  # Find all the faces in the current frame of video
          for top, right, bottom, left in self.face_locations: # Display the results
              cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) # Draw a box around the face
              encoded, buffer = cv2.imencode('.jpg', frame)
              return buffer

    def ReadCameraLoop(self):
        while True:
            ret, frame = self.video_capture.read() # Grab a single frame of video
            n.stream(self.EncodeImg(frame))
           # cv2.imshow("video",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): # Hit 'q' on the keyboard to quit!
                self.__del__()
                break

    def EncodeImg(self, img):
        retval, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text

    def stream(self, buffer):
        retval, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        enc = base64.urlsafe_b64encode(buffer)

    def __del__(self):
        self.video_capture.release() # Release handle to the webcam
        cv2.destroyAllWindows()
        logger.debug('Destructor network class')


if __name__=='__main__':
    n = Network()
    if n.Status:
        openCV = Open_Cv()
    else:
        logger.critical("Failed to start")



