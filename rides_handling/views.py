from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from rides_handling.forms import SignUpForm

@login_required
def home(request):
    return render(request, 'home.html')

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
            user.profile.is_driver = form.cleaned_data.get('is_driver')
            user.profile.car = form.cleaned_data.get('car')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def offer (request):
    return render(request, 'offer.html')

@login_required
def signup_driver (request):
    return render(request, 'signup_driver.html')
 