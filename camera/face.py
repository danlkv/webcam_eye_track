import cv2
import numpy as np
import argparse

def read_cascade_files(face_file, eye_file):
    face_cascade = cv2.CascadeClassifier(face_file)
    eye_cascade = cv2.CascadeClassifier(eye_file)
    return face_cascade, eye_cascade
#consider increasing FPS https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

def getAvailableCameraIds(max_to_test):
    available_ids = []
    for i in range(max_to_test):
        temp_camera = cv2.VideoCapture(i)
        if temp_camera.isOpened():
            temp_camera.release()
            print ("found camera with id %d"%i)
            available_ids.append(i)
    return available_ids

class Camera():
    def __init__(self,cam_id,
            width=640,
            height=640,
            faces=None,
            eyes=None,
            ):
        """
        Init an ifc for camera with face and eye
        detection
        Throws: string
        """
        if not id:
            raise Exception("You need to specify camera Id")
        print("starting Camera",cam_id)
        self.cap = cv2.VideoCapture(cam_id)
        self.cap.set(3,width) # set Width
        self.cap.set(4,height) # set Height
        if faces and eyes:
            print("Initing face and eye detection")
            self.faces,self.eyes = read_cascade_files(faces,eyes)



    def read(self):
        """
        Reads data from camera
        """
        ret, img = self.cap.read()
        return img

    def detect(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faces.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
            )
        eyes = []
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            # detect Eyes
            eyes = self.eyes.detectMultiScale(roi_gray)
        return faces,eyes

    def get_imgs(self,img,faces,eyes):
        fs,es = [],[]
        for (x,y,w,h) in faces:
            roi_color = img[y:y+h, x:x+w]
            fs.append(roi_color)
            for (ex,ey,ew,eh) in eyes:
                es.append(roi_color[ey:ey+eh, ex:ex+ew])
        return fs,es

    def draw_rects(self,img,faces,eyes):
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_color = img[y:y+h, x:x+w]
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        return img

    def show(self,img):
        """
        img: array
            image to show

        Throws: str if esc key pressed
        """
        cv2.imshow('video',img)
        k = cv2.waitKey(20) & 0xff
        if k == 27: # press 'ESC' to quit
            raise Exception("ESC pressed")
