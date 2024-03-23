from django.http import HttpResponse
from django.shortcuts import render
from . import models
from conversion_model import code1
from presenting_model import code2
from presenting_model.code2 import cv2
import keyboard
from keypress_model.code3 import on_key_press

# Create your views here.

def home(request):
    brand1 = models.brands()
    brand1.name = "maruti suzuki"
    brand1.available = True
    
    brand2 = models.brands()
    brand2.name = "splendor"
    brand2.available = False

    brand3 = models.brands()
    brand3.name = "cycle"
    brand3.available = True

    brand4 = models.brands()
    brand4.name = "auto-rickshaw"
    brand4.available = True

    the_brands = [brand1 , brand2 , brand3 , brand4]

    return render(request, "home_screen1.html", {"the_brands" : the_brands})

def proceed(request):
    pdf_file_path = 'conversion_model\input\BloodLink_50.pdf'
    output_folder_path = 'conversion_model\output'

    code1.convert_pdf_to_png(pdf_file_path, output_folder_path, target_width=1280, target_height=720)

    return render(request, "present_page.html")

def present(request):
    code2.present_slides()  
    return render(request, "home_screen1.html")



