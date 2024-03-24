from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import UserLogForm, UserRegForm



def homepage(request):
    return render(request, 'reg_log/home.html')


def user_registration(request):
    form = UserRegForm()
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
            
    

    return render(request, 'reg_log/registration.html', {'form':form})

def user_login(request):
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'],
                                password = cd['password1'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('mainPage'))
            

    else:
        form = UserLogForm()



    return render(request, 'reg_log/login.html', {'form':form})
