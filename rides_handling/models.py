from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_driver = models.BooleanField(default=False, blank=True)
	car = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.user.username

class Ride(models.Model):
	set_by_driver = 'SET_BY_DRIVER'
	set_by_passenger = 'SET_BY_PASSENGER'
	accepted = 'ACCEPTED'
	completed = 'COMPLETED'

	STATUS_CHOICES = (
		(set_by_driver, 'set by driver'),
		(set_by_passenger, 'set by passenger'),
		(accepted, 'accepted'),
		(completed, 'completed')
	)

	initiator = models.ForeignKey(Profile, on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	start_data = models.DateField()
	pickup_longitude = models.DecimalField(max_digits=5, decimal_places=2)
	pickup_latitude = models.DecimalField(max_digits=5, decimal_places=2)
	dropoff_longitude = models.DecimalField(max_digits=5, decimal_places=2)
	dropoff_latitude = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return ('({}, {}) -> ({}, {}) {}'.format(self.pickup_longitude, self.pickup_latitude, 
												self.dropoff_longitude, self.dropoff_latitude, self.status))

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()