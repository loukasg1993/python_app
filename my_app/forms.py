from django import forms
from .models import personal_information,appointment


class Createform(forms.ModelForm):

    class Meta:
        model= personal_information
        fields= ['id','age','name',
                 'sex','height','weight','bmi','children','smoker','region','charges','telephone_no','address']

class Createappointment(forms.ModelForm):

    class Meta:
        model= appointment
        fields= ['id','amka', 'bmi', 'dose', 'date']
