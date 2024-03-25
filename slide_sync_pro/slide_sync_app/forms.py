
from django.forms import ModelForm
from . models import Uploadfile



class UploadForm(ModelForm):
    class Meta:
        model = Uploadfile
        fields = '__all__'