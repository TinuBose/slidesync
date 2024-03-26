from urllib import request
from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
from slide_sync_app.delete_file import file_delete
from django.shortcuts import redirect, render

def present_slides():
    width, height = 1280, 520
    gestureThreshold = 300
    folderPath = "conversion_model\output"
    

    
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    
    detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

   
    imgList = []
    delay = 30
    buttonPressed = False
    counter = 0
    drawMode = False
    imgNumber = 0
    delayCounter = 0
    annotations = [[]]
    annotationNumber = -1
    annotationStart = False
    hs, ws = int(120 * 1), int(213 * 1)  

    
    zoomScale = 1.0
    zoomSpeed = 0.02

    
    pathImages = sorted(os.listdir(folderPath), key=len)
    print(pathImages)

    while True:
       
        success, img = cap.read()
        img = cv2.flip(img, 1)
        pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
        imgCurrent = cv2.imread(pathFullImage)

       
        hands, img = detectorHand.findHands(img) 
       
        cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

        if hands and buttonPressed is False:  

            hand = hands[0]
            cx, cy = hand["center"]
            lmList = hand["lmList"]  
            fingers = detectorHand.fingersUp(hand) 

          
            xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
            yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
            indexFinger = xVal, yVal

            if cy <= gestureThreshold:  
                if fingers == [1, 0, 0, 0, 0]:
                    print("Left")
                    buttonPressed = True
                    if imgNumber > 0:
                        imgNumber -= 1
                        annotations = [[]]
                        annotationNumber = -1
                        annotationStart = False
                if fingers == [0, 0, 0, 0, 1]:
                    print("Right")
                    buttonPressed = True
                    if imgNumber < len(pathImages) - 1:
                        imgNumber += 1
                        annotations = [[]]
                        annotationNumber = -1
                        annotationStart = False



        if buttonPressed:
            counter += 1
            if counter > delay:
                counter = 0
                buttonPressed = False

        for i, annotation in enumerate(annotations):
            for j in range(len(annotation)):
                if j != 0:
                    cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

        imgCurrent = cv2.resize(imgCurrent, None, fx=zoomScale, fy=zoomScale)

        imgSmall = cv2.resize(img, (ws, hs))
        h, w, _ = imgCurrent.shape
        imgCurrent[0:hs, w - ws: w] = imgSmall

        cv2.imshow("Slides", imgCurrent)
        cv2.imshow("Image", img)
        


        key = cv2.waitKey(1)
        if key == ord('q'):
            break
 
    cv2.destroyAllWindows()
