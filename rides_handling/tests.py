from django.test import TestCase, RequestFactory
from .forms import SignUpForm, RideForm, SignUpDriverForm
from django.contrib.auth.models import User
from django.test import Client
from .models import Profile
from django.contrib.auth.models import User, AnonymousUser
from .apps import RidesHandlingConfig
from django.apps import apps
from django.urls import reverse

from .views import signup_driver

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
    

class ViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345blablasd')
        user.save()

    def test_user_log_in(self):
        c = Client()
        logged_in = c.login(username='testuser', password='12345blablasd')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_can_log_out(self):
        c = Client()
        logged_in = c.login(username='testuser', password='12345blablasd')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_view_template_get(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_wrong_signup(self):
        response1 = self.client.post(reverse('signup'), {'username': '', 'password1': 'verygoodpass123', 'password_2': 'verygoodpass123'}, follow=True)
        self.assertTemplateUsed(response1, 'signup.html')
        response2 = self.client.post(reverse('signup'), {'username': 'fafaf',  'password1':  'verygoodpass123',  'password_2':  'verygoodpass123'}, follow=True)
        self.assertTemplateUsed(response2, 'signup.html')  
        response3 = self.client.post(reverse('signup'), {'username': 'user1',  'password1': 'verygoodpass123',  'password_2': 'verygoodpass123'}, follow=True)
        self.assertTemplateUsed(response3, 'signup.html')

    def test_home_page_if_not_logged_in(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_about_page(self):
        response = self.client.get(reverse('about'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_help_page(self):
        response = self.client.get(reverse('help'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'help.html')

    def test_profile_summary_if_not_logged_in(self):
        response = self.client.get(reverse('profile_summary'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
class SimpleTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser', password='secret')

    def test_signup_driver_anonymous(self):
        request = self.factory.get('/signup_driver')
        request.user = AnonymousUser()
        response = signup_driver(request)
        self.assertEqual(response.status_code, 302)
    def test_signup_driver_logged_in(self):
        request = self.factory.get('/signup_driver')
        request.user = self.user
        response = signup_driver(request)
        self.assertEqual(response.status_code, 200)
    def test_signup_driver_already_driver(self):
        response = self.client.post('/signup_driver', {'is_driver': 'True','car': 'ford'})
        self.assertEqual(response.status_code, 301)
