from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from rides_handling.forms import SignUpForm, RideForm, SignUpForm, SignUpDriverForm
from django.utils import timezone
from .models import Profile, Ride

from sklearn.externals import joblib
import numpy as np
import datetime

def euklidian_distance(a_x,a_y,b_x,b_y):
    return np.sqrt((a_x - b_x)**2 + (a_y - b_y)**2)

def manhattan_distance(a_x,a_y,b_x,b_y):
    return np.absolute(a_x - b_x) + np.absolute(a_y - b_y)


@login_required
def home(request):
    if request.method == "POST":
        regressor = joblib.load('rides_handling/production_full.pkl')
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            try:
                ride.initiator = request.user.profile
            except Profile.DoesNotExist:
                ride.initiator = Profile(user=request.user)
            ride.status = 'SET_BY_PASSENGER'
            ride.pickup_datetime = timezone.now()

            now = datetime.datetime.now()
            ml_input = np.array([
            ride.pickup_longitude,
            ride.pickup_latitude,
            ride.dropoff_longitude,
            ride.dropoff_latitude,
            now.hour, now.month, 
            euklidian_distance(ride.pickup_longitude, ride.pickup_latitude, ride.dropoff_longitude, ride.dropoff_latitude),
            manhattan_distance(ride.pickup_longitude, ride.pickup_latitude, ride.dropoff_longitude, ride.dropoff_latitude),
            ])
            ride.estimated_trip_time = np.exp(regressor.predict([ml_input])[0]) / 60
            
            
            ride.save()
            return redirect('profile_summary')
    else:
        form = RideForm()
        rides_history = request.user.profile.ride_set.all()
        rides_history = list(reversed(rides_history))
        if not rides_history:
            recent_ride_status = "no rides"
        else:
            recent_ride_status = rides_history[0].status
        return render(request, 'home.html', {'form' : form, 'rides_history' : rides_history, 'recent_ride_status' : recent_ride_status })


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.is_driver = False
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def offer(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.user.profile.is_driver == True:
            rides_active = Ride.objects.filter(status='SET_BY_PASSENGER').all()

            if request.POST:
                pk_number = int(request.POST['take'].strip(','))
                ride = Ride.objects.get(pk=pk_number)
                ride.status = 'ACCEPTED'
                ride.driver = request.user.profile
                ride.save()
                return redirect('profile_summary')

            return render(request, 'offer.html', {'rides_active' : rides_active})
        return redirect('signup_driver')

def help(request): 
    return render(request, 'help.html')
    
def about(request): 
    return render(request, 'about.html')

def signup_driver(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = SignUpDriverForm(request.POST, instance = request.user.profile)
            if form.is_valid():
                user = form.save(commit = False)
                user.refresh_from_db()
                user.is_driver = True
                user.car = form.cleaned_data.get('car')
                user.save()
                return redirect('offer')
        else:
            form = SignUpDriverForm()
        return render(request, 'signup_driver.html')

@login_required
def profile_summary(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        if request.GET.get('finish'):
            rides_history = list(request.user.profile.ride_set.all())
            rides_history.extend(Ride.objects.filter(driver=request.user.profile).all())
            for ride in rides_history:
                if ride.status == 'ACCEPTED' or ride.status == 'SET_BY_PASSENGER':
                    ride.status = 'COMPLETED'
                    ride.save()
            return redirect('profile_summary')
        if request.GET.get('cancel'):
            rides_history = list(request.user.profile.ride_set.all())
            rides_history.extend(Ride.objects.filter(driver=request.user.profile).all())
            for ride in rides_history:
                if ride.status == 'ACCEPTED' or ride.status == 'SET_BY_PASSENGER' :
                    ride.status = 'CANCELED'
                    ride.save()
            return redirect('profile_summary')            

        rides_history = list(reversed(request.user.profile.ride_set.all()))
        rides_history_as_driver = list(reversed(Ride.objects.filter(driver=request.user.profile)))

        if not rides_history:
            recent_ride_status = "no rides"
        else:
            recent_ride_status = rides_history[0].status
        return render(request, 'profile_summary.html', {'user' : request.user, 'rides_history' : rides_history, 'rides_history_as_driver' : rides_history_as_driver, 'recent_ride_status': recent_ride_status })
        
