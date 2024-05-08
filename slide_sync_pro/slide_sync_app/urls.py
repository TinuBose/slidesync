from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.home,name='home'),
    path('proceed', views.proceed,name='proceed'),
    # path('present', views.present,name='present'),
    path('presenting', views.presenting,name='presenting'),
    path('check_stop_presentation', views.check_stop_presentation,name='check_stop_presentation'),
    path('gesture', views.gesture, name='gesture')
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)