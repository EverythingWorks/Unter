from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ride

class SignUpForm(UserCreationForm):
    is_driver = forms.BooleanField(required=False, help_text='Do you want to share a car?')
    car = forms.CharField(required=False, help_text='Your car')

    class Meta:
        model = User
        fields = ('username', 'is_driver', 'car', 'password1', 'password2', )

class SignUpDriverForm(forms.ModelForm):
    is_driver = forms.BooleanField(required=False)
    car = forms.CharField()
    
    class Meta:
        model = User
        fields = ('is_driver', 'car',)

class RideForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RideForm, self).__init__(*args, **kwargs)
        self.fields['passenger_count'].widget.attrs['min'] = 1
    
    def clean_passenger_count(self):
        passenger_count = self.cleaned_data['passenger_count']
        if passenger_count < 1:
            raise forms.ValidationError("Passenger count cannot be less than 1")
        return passenger_count

    class Meta:
        model = Ride
        fields =  ( 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count', )