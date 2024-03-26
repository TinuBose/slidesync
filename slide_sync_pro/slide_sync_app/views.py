from django.http import HttpResponse
from django.shortcuts import redirect, render

from filename_model import file_name  
from . import models
from conversion_model import code1
from presenting_model import code2
from presenting_model.code2 import cv2
from .forms import UploadForm
import threading


# Create your views here.


def home(request):
    return render(request, "home_screen1.html")

def proceed(request):
    if request.POST:
        frm = UploadForm(request.POST)
        if frm.is_valid():
            frm.save()
    else:
        frm = UploadForm


    folder_path = 'conversion_model\input'  
    the_filename = file_name.get_file_names(folder_path)
    print(the_filename)
    pdf_file_path = 'conversion_model\input\{}'.format(the_filename)
    output_folder_path = 'conversion_model\output'

    code1.convert_pdf_to_png(pdf_file_path, output_folder_path, target_width=1280, target_height=720)

    return render(request, "present_page.html")


def presenting(request):
    
    def present_slides_in_thread():
        print("starting")
        code2.present_slides()
        print("end")



    presentation_thread = threading.Thread(target=present_slides_in_thread)
    
  
    print("starting the thread")
    presentation_thread.start()
    
    return render(request, "presenting_page.html")


    



