from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')

def user_info(request):
    return render(request, 'main/user.html')




    