from django.test import TestCase, RequestFactory
from .forms import SignUpForm, RideForm, SignUpDriverForm
from django.contrib.auth.models import User
from django.test import Client
from .models import Profile, Ride
from django.contrib.auth.models import User, AnonymousUser
from .apps import RidesHandlingConfig
from django.apps import apps
from django.urls import reverse
from .views import order_ride, signup_driver, signup, get_address
from django.utils import timezone
from .views import cancel_ride, finish_ride
from .admin import CustomUserAdmin

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
        good_form3 = RideForm(data={'pickup_longitude' : 44.84, 'pickup_latitude' : 60.165, 'dropoff_longitude' : -55.155, 'dropoff_latitude' : 55.96, 'passenger_count' : 4, })
        self.assertTrue(good_form3.is_valid())
        good_form4 = RideForm(data={'pickup_longitude' : 11, 'pickup_latitude' : 12, 'dropoff_longitude' : 12, 'dropoff_latitude' : 11, 'passenger_count' : 2, })
        self.assertTrue(good_form4.is_valid())

    def test_if_ride_form_is_invalid(self):
        wrong_form1 = RideForm(data={'pickup_longitude' : 0, 'pickup_latitude' : 0, 'dropoff_longitude' : 0, 'dropoff_latitude' : 0, 'passenger_count' : -5, })
        self.assertFalse(wrong_form1.is_valid())
        wrong_form2 = RideForm(data={'pickup_longitude' : 1555555, 'pickup_latitude' : 0, 'dropoff_longitude' : 0, 'dropoff_latitude' : 0, 'passenger_count' : -5, })
        self.assertFalse(wrong_form2.is_valid())
        wrong_form3 = RideForm(data={'pickup_longitude' : 1555555, 'pickup_latitude' : 0, 'dropoff_longitude' : 0, 'dropoff_latitude' : 0,})
        self.assertFalse(wrong_form3.is_valid())
        wrong_form4 = RideForm()
        self.assertFalse(wrong_form4.is_valid())
        wrong_form5 = RideForm(data={'pickup_longitude' : 1555555, 'pickup_latitude' : 111111111, 'dropoff_longitude' : -323, 'dropoff_latitude' : 12, 'passenger_count' : 1,})
        self.assertFalse(wrong_form5.is_valid())
        wrong_form6 = RideForm(data={'dropoff_longitude' : 0, 'dropoff_latitude' : 0, 'passenger_count' : 3,})
        self.assertFalse(wrong_form6.is_valid())


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
    
    def test_post_good_signup(self):
        data = {'username' : 'nowyuser', 'is_driver' : True, 'car' : 'skoda',  'password1': 'strongpass1', 'password2': 'strongpass1',}
        c = Client()
        url = reverse('signup')
        response = c.post(url, data, format='json')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
    
    def test_signup_authenticated(self):
        factory = RequestFactory()
        request = factory.get('/signup')
        user = User.objects.create(username='testuser1')
        user.set_password('12345blablasd')
        request.user = user
        response = signup(request)
        self.assertEqual(response.status_code, 302)

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

    def test_login_already_logged_in(self):
        client = Client()
        client.login(username='testuser', password='12345blablasd')
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class UserModelTest(TestCase):
    def test_str_method(self):
        user = User.objects.create(username='test2user')
        user.set_password('12345blablasd')
        user.save()
        self.assertEqual(str(user), 'test2user')

class TestSignupDriver(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser', email='testmail@domain.com')
        self.user.set_password('secretpass123')
        self.user.save()

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
        data = {
            'is_driver': True,
            'car': 'ford'
                }
        c = Client()
        logged_in = c.login(username='testuser', password='secretpass123')
        url = reverse('signup_driver')
        response = c.post(url, data, format='json')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/offer/')

class TestOffer(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='testmail@domain.com')
        self.user.set_password('secretpass123')
        self.user.save()
        self.url = reverse('offer')
        
        self.ride = Ride()
        self.ride.initiator = self.user.profile
        self.ride.status = 'ACCEPTED'
        self.ride.driver = self.user.profile
        self.ride.pickup_longitude = 1
        self.ride.pickup_latitude = 1
        self.ride.dropoff_longitude = 1
        self.ride.dropoff_latitude = 1
        self.ride.pickup_datetime = timezone.now()
        self.ride.passenger_count = 1


    def test_signup_anonymous(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_user_not_driver(self):
        client = Client()
        client.login(username='testuser', password='secretpass123')
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/signup_driver/')

        
    def test_driver_no_rides(self):
        self.user.profile.is_driver = True
        self.user.save()
        client = Client()
        logged_in = client.login(username='testuser', password='secretpass123')  
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'offer.html')

    def test_offer_post(self):
        self.ride.save()
        self.user.profile.is_driver = True
        self.user.save()
        client = Client()
        logged_in = client.login(username='testuser', password='secretpass123')
        
        data = {'take': '1'}
        response = client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/chat/1/")

class TestHome(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='testmail@domain.com')
        self.user.set_password('secretpass123')
        self.user.save()
        self.url = reverse('home')
        self.factory = RequestFactory()

        self.ride = Ride()
        self.ride.initiator = self.user.profile
        self.ride.status = 'ACCEPTED'
        self.ride.driver = self.user.profile
        self.ride.pickup_longitude = 1
        self.ride.pickup_latitude = 1
        self.ride.dropoff_longitude = 1
        self.ride.dropoff_latitude = 1
        self.ride.pickup_datetime = timezone.now()
        self.ride.passenger_count = 1

    def test_order_ride_good_form(self):
        good_form = RideForm(data={
            'pickup_longitude' : 0, 
            'pickup_latitude' : 0, 
            'dropoff_longitude' : 0, 
            'dropoff_latitude' : 0, 
            'passenger_count' : 1,
            })
        request = self.factory.get(self.url)
        request.user = self.user
        self.assertTrue(order_ride(good_form, request))
        
    def test_order_ride_bad_form(self):
        wrong_form = RideForm(data={
            'pickup_longitude' : 1555555, 
            'pickup_latitude' : 0, 
            'dropoff_longitude' : 0, 
            'dropoff_latitude' : 0, 
            'passenger_count' : 1,
            })
        request = self.factory.get(self.url)
        request.user = self.user
        self.assertFalse(order_ride(wrong_form, request))

    def test_post_ride(self):
        data={
            'pickup_longitude' : 0, 
            'pickup_latitude' : 0, 
            'dropoff_longitude' : 0, 
            'dropoff_latitude' : 0, 
            'passenger_count' : 1,
            }
        c = Client()
        logged_in = c.login(username='testuser', password='secretpass123')
        response = c.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile_summary/')
    
    def test_home_has_rides(self):
        self.ride.save()
        c = Client()
        logged_in = c.login(username='testuser', password='secretpass123')
        response = c.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/chat/1/')
    
    def test_home_no_rides(self):
        c = Client()
        logged_in = c.login(username='testuser', password='secretpass123')
        response = c.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

class TestProfileSummary(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='testmail@domain.com')
        self.user.set_password('secretpass123')
        self.user.profile.is_driver = True
        self.user.save()
        self.url = reverse('profile_summary')
        self.factory = RequestFactory()

        self.ride = Ride()
        self.ride.initiator = self.user.profile
        self.ride.status = 'ACCEPTED'
        self.ride.driver = self.user.profile
        self.ride.pickup_longitude = 1
        self.ride.pickup_latitude = 1
        self.ride.dropoff_longitude = 1
        self.ride.dropoff_latitude = 1
        self.ride.pickup_datetime = timezone.now()
        self.ride.passenger_count = 1

    

    def test_signup_anonymous(self):
        c = Client()
        response = c.get(reverse('profile_summary'))
        self.assertEqual(response.status_code, 302)

    def test_cancel_ride_good(self):
        client = Client()
        logged_in = client.login(username='testuser', password='secretpass123')
        history = [self.ride]
        result, history = cancel_ride(history)
        self.assertEqual(result, 1)
        self.assertEqual(history[0].status, 'CANCELED')
        
    def test_cancel_ride_bad(self):
        client = Client()
        logged_in = client.login(username='testuser', password='secretpass123')
        self.ride.status = 'CANCELED'
        history = [self.ride]
        result, new_history = cancel_ride(history)
        new_status = new_history[0].status
        self.assertEqual(result, 0)
        self.assertEqual(new_status, 'CANCELED')

    def test_fnish_ride_good(self):
        request = self.factory.get('/profile_summary')
        request.user = self.user
        grades = [2]
        request.GET = {'grade' : grades}
        history = [self.ride]
        result, new_history = finish_ride(history, request)
        new_status = new_history[0].status
        self.assertEqual(result, 1)
        self.assertEqual(new_status, 'COMPLETED')
        
    def test_fnish_ride_bad(self):
        request = self.factory.get('/profile_summary')
        request.user = self.user
        grades = [2]
        request.GET = {'grade' : grades}
        self.ride.status = 'CANCELED'
        history = [self.ride]
        result, new_history = finish_ride(history, request)
        new_status = new_history[0].status
        self.assertEqual(result, 0)
        self.assertEqual(new_status, 'CANCELED')
        
        

class TestGettingAddress(TestCase):
    def test_parsing(self):
        address = "29, Avenue, Green Valley"
        data = {'address' : {'house_number': '29', 'suburb': 'Green Valley', 'road': 'Avenue'}, 'other_key': 'to_be_skipped'}
        self.assertEqual(get_address(data), address)

