from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('proceed', views.proceed,name='proceed')
]
