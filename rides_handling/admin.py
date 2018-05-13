from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Ride

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_is_driver(self, instance):
        return instance.profile.is_driver
    get_is_driver.short_description = 'is_driver'

    def get_car(self, instance):
        return instance.profile.car
    get_car.short_description = 'Car'

    list_display = ('username', 'get_is_driver', 'get_car', 'is_staff')
    list_select_related = ('profile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class RidesAdmin(admin.ModelAdmin):
	list_display = ('initiator', 'driver', 'status', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'pickup_datetime', 'passenger_count','estimated_trip_time')
	list_filter = ('status',)
	date_hierarchy = 'pickup_datetime'
	ordering = ['-pickup_datetime', 'status']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Ride, RidesAdmin)
