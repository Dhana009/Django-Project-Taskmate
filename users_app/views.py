from django.shortcuts import render, redirect
from .forms import Customregisterform
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == "POST":
        register_form = Customregisterform(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, ('new user account created, login to get started'))
            return redirect('register')
    else:
        register_form = Customregisterform()
    return render(request, 'register.html', {'register_form': register_form})
