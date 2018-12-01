import cv2
import numpy as np
import argparse

face_cascade = cv2.CascadeClassifier('/home/danlkv/Junction/payhere/ml_data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/danlkv/Junction/payhere/ml_data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('/home/danlkv/Junction/payhere/ml_data/haarcascade_smile.xml')

def main(
        gui=False,
        smiles = False
        ):
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    print('starting...')
    while True:
        ret, img = cap.read()
        #img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
            )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            # detect Eyes
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            if smiles:
            # detect Smile
                smiles = smile_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in smiles:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,100,255),2)

        if gui:
            cv2.imshow('video',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    if gui:
        cv2.destroyAllWindows()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='GUI?')
    parser.add_argument('--gui',dest='gui', action="store_true",default=False)
    parser.add_argument('--smiles',dest='smiles', action="store_true",default=False)
    args = parser.parse_args()

    if args.gui:
        print("starting with gui")
        main(gui=True,smiles=args.smiles)
    else:
        main(gui=False,smiles=args.smiles)
