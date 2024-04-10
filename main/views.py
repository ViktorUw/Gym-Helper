from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):
    return render(request, 'main/index.html')

def user_info(request):
    return render(request, 'main/user.html')

def trainings(request):
    return render(request, 'main/trainings.html')

def training_plans(request):
    return render(request, 'main/training_plans.html')
    