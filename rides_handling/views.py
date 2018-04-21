from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from rides_handling.forms import SignUpForm, RideForm 
from django.utils import timezone
from .models import Profile

@login_required
def home(request):
    if request.method == "POST":
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            try:
                ride.initiator = request.user.profile
            except Profile.DoesNotExist:
                ride.initiator = Profile(user=request.user)
            
            ride.pickup_datetime = timezone.now()
            ride.save()
            return redirect('profile_summary')
    else:
        form = RideForm()
        return render(request, 'home.html', {'form' : form, })


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
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                if user.profile.is_driver == True:
                    return render(request, 'offer.html')
                else:
                    return render(request, 'signup_driver.html')
        else:
            form = SignUpForm()
        return render(request, 'signup_driver.html')
    

@login_required
def signup_driver(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.profile.is_driver = True
                user.profile.car = form.cleaned_data.get('car')
                user.save()
                return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'signup_driver.html')
 

def profile_summary(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        rides_history = request.user.profile.ride_set.all()
        return render(request, 'profile_summary.html', {'user' : request.user, 'rides_history' : rides_history, })
   