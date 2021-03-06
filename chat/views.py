from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from chat.forms import MessageForm
from rides_handling.models import Ride

def chat(request, pk):
    ride = get_object_or_404(Ride, pk=pk)
    if request.user.pk != ride.initiator.pk and request.user.pk != ride.driver.pk:
        return redirect('profile_summary')
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.ride = ride
            message.user = request.user
            message.save()
            return redirect('chat', pk=ride.pk)
    else:
        form = MessageForm()
    return render(request, 'chat.html', {'form': form, 'ride': ride})
