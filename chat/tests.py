from django.test import TestCase, RequestFactory
from django.apps import apps
from .apps import ChatConfig
from .forms import MessageForm
from .models import Message
from django.utils import timezone
from django.contrib.auth.models import User
from rides_handling.models import Ride
from .views import chat

class ChatConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ChatConfig.name, 'chat')
        self.assertEqual(apps.get_app_config('chat').name, 'chat')


class MessageFormTest(TestCase):
    def test_if_message_form_is_valid(self):
        good_form = MessageForm(data={'content' : 'blabh blabh'})
        self.assertTrue(good_form.is_valid())

class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
        self.user = User.objects.create(username='testuser', email='testmail@domain.com')
        self.user.set_password('secretpass123')
        self.user.save()

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
        self.ride.save()

    def test_chat_post(self):
        data = {'content':'hello',}
        request = self.factory.post('/', data)
        request.user =self.user
        request.method = 'POST'
        response = chat(request, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/1/")
    
class TestModel(TestCase):
    def setUp(self):
        self.message = Message()
        self.message.content = "hello"
    
    def test_str(self):
        self.assertEqual("hello", self.message.__str__())
        
