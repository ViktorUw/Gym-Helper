from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
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
            messages.success(request, 'You are registered successfully')
            return HttpResponseRedirect(reverse('login'))
        else:

            for field in form.errors:
                field_errors = ', '.join([str(err) for err in form.errors[field]])
                messages.error(request, f"{field} : {field_errors}")
    else:
        form = UserRegForm()    
        
        
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
                messages.success(request, 'You are logged in successfully')
                return HttpResponseRedirect(reverse('mainPage'))
            else:
                messages.error(request, 'Invalid login or password')
        
            

    else:
        form = UserLogForm()



    return render(request, 'reg_log/login.html', {'form':form})


def user_logout(request):
    logout(request)
    messages.success(request,'You are logged out successfully')
    return HttpResponseRedirect(reverse('login'))