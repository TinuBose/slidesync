from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from filename_model import file_name  
from . import models
from conversion_model import code1
from presenting_model import code2
from presenting_model.code2 import cv2
from .forms import UploadForm
import threading
from django.contrib import admin
from .models import Uploadfile   
from urllib import request
from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
from slide_sync_app.delete_file import file_delete
from django.shortcuts import redirect, render
from empty_folder_model import empty
from django.views.decorators.cache import cache_control 

# Create your views here.

stop_presentation = False


def home(request):
    global stop_presentation
    stop_presentation=False
    return render(request, "home_screen1.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def proceed(request):
    if request.method == 'POST':
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            new_upload=Uploadfile(upload=request.FILES['upload'])
            new_upload.save()
            folder_path = 'conversion_model\input\conversion_model\input'  
            the_filename = file_name.get_file_names(folder_path)
            print(the_filename)
            pdf_file_path = 'conversion_model\input\conversion_model\input\{}'.format(the_filename)
            output_folder_path = 'conversion_model\output'

            code1.convert_pdf_to_png(pdf_file_path, output_folder_path, target_width=1280, target_height=720)

            return render(request, "present_page.html")
        else:
            form=UploadForm()
            return render(request,'home_screen1.html')


def presenting(request):
    
    
    def present_slides_in_thread():
        print("starting")
        present_slides()
        print("end")

    presentation_thread = threading.Thread(target=present_slides_in_thread)
    
  
    presentation_thread.start()
    
    return render(request, "presenting_page.html")


def check_stop_presentation(request):
    global stop_presentation
    return JsonResponse({'stop_presentation': stop_presentation})



def present_slides():

    global stop_presentation

    width, height = 1280, 520
    gestureThreshold = 500
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
                if fingers == [0, 1, 1, 0, 0]:
                    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

                if fingers == [0, 1, 0, 0, 0]:
                    if annotationStart is False:
                        annotationStart = True
                        annotationNumber += 1
                        annotations.append([])
                    print(annotationNumber)
                    annotations[annotationNumber].append(indexFinger)
                    cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

                else:
                    annotationStart = False
                if fingers == [0, 1, 1, 1, 0]:
                    if annotations:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        buttonPressed = True

                        # Zoom Gesture
                if fingers == [0, 1, 1, 1, 1]:
                    zoomScale += zoomSpeed
                    print("Zoom In:", zoomScale)
                if fingers == [1, 1, 1, 1, 1]:
                    zoomScale -= zoomSpeed
                    if zoomScale < 1.0:
                        zoomScale = 1.0
                    print("Zoom Out:", zoomScale)




                



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
            stop_presentation = True
            break
        if stop_presentation:
            
            break
    
 
    cv2.destroyAllWindows()
    Uploadfile.objects.all().delete()
    empty.empty_folder('conversion_model\output')
    empty.empty_folder('conversion_model\input\conversion_model\input')
    



