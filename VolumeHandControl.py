import cv2
import time
import numpy as np
import math
import sys
import HandTrackingModule as htm
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#######################################
wCam,hCam=1920,1080
#######################################
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
detector=htm.handDetector(detectionCon=0.7)
try:
    while True:
        success,img=cap.read()
        img=detector.findHands(img)
        lmList=detector.findPosition(img,draw=False)
        if len(lmList)!=0:
            #print(lmList[4],lmList[8])
            x1,y1=lmList[4][1],lmList[4][2];
            x2, y2 = lmList[8][1], lmList[8][2];
            cx,cy=(x1+x2)//2,(y1+y2)//2
            cv2.circle(img,center=(x1,y1),radius=10,color=(255,0,255),thickness=cv2.FILLED)
            cv2.circle(img, center=(x2,y2), radius=10,color=(255,0,255),thickness=cv2.FILLED)
            cv2.circle(img, center=(cx, cy), radius=10, color=(255, 0, 255), thickness=cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            length=math.hypot(x2-x1,y2-y1)
            #print(length,'-------')
            #print(length)
            #handrange=  50-300
            #volrange- -65 -0
            vol=np.interp(length,[50,300],[minVol,maxVol])
            volBar=np.interp(length,[50,300],[400,150])
            volPer=int(np.interp(length,[50,300],[0,100]))
            volume.SetMasterVolumeLevel(vol, None)
            if(length<=50):
                cv2.circle(img, center=(cx, cy), radius=10, color=(0, 255, 0), thickness=cv2.FILLED)
            cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
            cv2.rectangle(img, (50,int(volBar) ), (85, 400),(255,0,0),cv2.FILLED);
            cv2.putText(img, f'{volPer} %', (40, 450), cv2.FONT_ITALIC, 1, (255, 0, 0), 3)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img,f'FPS{int(fps)}',(40,50),cv2.FONT_ITALIC,1,(255,0,0),3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
except KeyboardInterrupt:sys.exit(0);