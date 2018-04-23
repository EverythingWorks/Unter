from django.test import TestCase
from .forms import SignUpForm, RideForm
from django.contrib.auth.models import User
from django.test import Client
from .models import Profile
from django.contrib.auth.models import User
from .apps import RidesHandlingConfig
from django.apps import apps

class SignupFormTest(TestCase):
    def test_if_signup_form_is_valid(self):
        good_form = SignUpForm(data={'is_driver' : False, 'username' : 'admin', 'password1' : 'admin123%.', 'password2' : 'admin123%.'})
        self.assertTrue(good_form.is_valid())

    def test_if_signup_form_is_invalid(self):
        wrong_form1 = SignUpForm(data={'is_driver' : False, 'username' : 'admin', 'password1' : 'short', 'password2' : 'short'})
        self.assertFalse(wrong_form1.is_valid())
        wrong_form2 = SignUpForm(data={'is_driver' : False, 'username' : 'admin', 'password1' : 'firstpassword', 'password2' : 'secondisdifferent'})
        self.assertFalse(wrong_form2.is_valid())


class RideFormTest(TestCase):
    def test_if_ride_form_is_valid(self):
        good_form1 = RideForm(data={'pickup_longitude' : 0, 'pickup_latitude' : 0, 'dropoff_longitude' : 0, 'dropoff_latitude' : 0, 'passenger_count' : 1, })
        self.assertTrue(good_form1.is_valid())
        good_form2 = RideForm(data={'pickup_longitude' : -10.10, 'pickup_latitude' : -10.1565, 'dropoff_longitude' : -10.155, 'dropoff_latitude' : 15.26, 'passenger_count' : 3, })
        self.assertTrue(good_form2.is_valid())

    def test_if_ride_form_is_invalid(self):
        wrong_form1 = RideForm(data={'pickup_longitude' : 0, 'pickup_latitude' : 0, 'dropoff_longitude' : 0, 'dropoff_latitude' : 0, 'passenger_count' : -5, })
        self.assertFalse(wrong_form1.is_valid())
        wrong_form2 = RideForm(data={'pickup_longitude' : 1555555, 'pickup_latitude' : 0, 'dropoff_longitude' : 0, 'dropoff_latitude' : 0, 'passenger_count' : -5, })
        self.assertFalse(wrong_form2.is_valid())
        wrong_form3 = RideForm(data={'pickup_longitude' : 1555555, 'pickup_latitude' : 0, 'dropoff_longitude' : 0, 'dropoff_latitude' : 0,})
        self.assertFalse(wrong_form3.is_valid())
        wrong_form4 = RideForm()
        self.assertFalse(wrong_form4.is_valid())


class RidesHandlingConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(RidesHandlingConfig.name, 'rides_handling')
        self.assertEqual(apps.get_app_config('rides_handling').name, 'rides_handling')
