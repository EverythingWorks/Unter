from django.test import TestCase
from django.apps import apps
from .apps import ChatConfig
from .forms import MessageForm
from .models import Message

class ChatConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ChatConfig.name, 'chat')
        self.assertEqual(apps.get_app_config('chat').name, 'chat')


class MessageFormTest(TestCase):
    def test_if_message_form_is_valid(self):
        good_form = MessageForm(data={'content' : 'blabh blabh'})
        self.assertTrue(good_form.is_valid())
