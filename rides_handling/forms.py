from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ride

class SignUpForm(UserCreationForm):
    is_driver = forms.BooleanField(required=False, help_text='Do you want to share a car?')
    car = forms.CharField(required=False, help_text='Your car')

    class Meta:
        model = User
        fields = ('username', 'is_driver', 'password1', 'password2', )


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields =  ( 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count', )