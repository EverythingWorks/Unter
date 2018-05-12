
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from rides_handling.forms import SignUpForm, RideForm, SignUpForm, SignUpDriverForm, AcceptRideForm
from django.utils import timezone
from .models import Profile, Ride

@login_required
def home(request):
    if request.method == "POST":
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            try:
                ride.initiator = request.user.profile
                ride.driver = request.user.profile
            except Profile.DoesNotExist:
                ride.initiator = Profile(user=request.user)
                ride.driver = Profile(user=request.user)
            ride.status = 'SET_BY_PASSENGER'
            ride.pickup_datetime = timezone.now()
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

            if request.GET:
                print(request.GET.get(...))
                # form = AcceptRideForm(request.POST)
                # print(form.errors)
                # if form.is_valid():
                #     ride = form.save(commit = False)
                #     # ride.refresh_from_db()
                #     ride.status = 'ACCEPTED'
                #     ride.save()
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
            rides_history = request.user.profile.ride_set.all()
            for ride in rides_history:
                if ride.status == 'ACCEPTED' or ride.status == 'SET_BY_PASSENGER':
                    ride.status = 'COMPLETED'
                    ride.save()
            return redirect('profile_summary')
        if request.GET.get('cancel'):
            rides_history = request.user.profile.ride_set.all()
            for ride in rides_history:
                if ride.status == 'ACCEPTED' or ride.status == 'SET_BY_PASSENGER' :
                    ride.status = 'CANCELED'
                    ride.save()
            return redirect('profile_summary')            

        rides_history = request.user.profile.ride_set.all()
        rides_history = list(reversed(rides_history))
        if not rides_history:
            recent_ride_status = "no rides"
        else:
            recent_ride_status = rides_history[0].status
        return render(request, 'profile_summary.html', {'user' : request.user, 'rides_history' : rides_history, 'recent_ride_status': recent_ride_status })
        