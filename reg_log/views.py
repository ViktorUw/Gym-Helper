from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import UserLogForm, UserRegForm


def homepage(request):
    return render(request, "reg_log/home.html")


def user_registration(request):
    form = UserRegForm()
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto zostało założone. Możesz się zalogować.")
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserRegForm()

    return render(request, "reg_log/registration.html", {"form": form})


def user_login(request):
    next_url = request.POST.get("next") or request.GET.get("next", "")
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["email"], password=cd["password1"])
            if user is not None:
                login(request, user)
                messages.success(request, "Zalogowano")
                if url_has_allowed_host_and_scheme(
                    next_url, allowed_hosts={request.get_host()}
                ):
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("mainPage"))

            else:
                messages.error(request, "Nieprawidłowy email lub hasło")

    else:
        form = UserLogForm()

    return render(request, "reg_log/login.html", {"form": form, "next": next_url})


@require_POST
def user_logout(request):
    logout(request)
    messages.success(request, "Wylogowano")
    return HttpResponseRedirect(reverse("login"))
