from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home_screen1.html")

def proceed(request):
    return render(request, "present_page.html")
