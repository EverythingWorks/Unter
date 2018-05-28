from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rides_handling.models import Ride


class Message(models.Model):
	ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='messages')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	date = models.DateTimeField(default=timezone.now)

	class Meta:
		ordering = ['date',]

	def __str__(self):
		return self.content
