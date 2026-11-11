from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from completed_trainings.forms import AdditionalWeight
from reg_log.forms import AccountForm
from reg_log.models import UserWeight

from .charts import line_chart


@login_required
def index(request):
    return render(request, 'main/index.html')

@login_required
def user_info(request):
    weight = list(UserWeight.objects.filter(user=request.user).order_by("date", "id"))
    last_weight = weight[-1] if weight else None

    graph = line_chart([w.date for w in weight], [w.weight for w in weight])

    return render(request, 'main/user.html', {
        'last_weight': last_weight,
        'weight': weight,
        # Newest first for the list under the chart
        'weight_history': weight[::-1],
        'graph': graph,
    })


@login_required
def edit_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane zostały zapisane")
            return redirect("userPage")
    else:
        form = AccountForm(instance=request.user)

    return render(request, "main/account_form.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Changing the password ends every session; keep this one logged in
            update_session_auth_hash(request, user)
            messages.success(request, "Hasło zostało zmienione")
            return redirect("userPage")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "main/password_form.html", {"form": form})


def get_user_weight(request, weight_id):
    """The user's own measurement, or 404 (also for someone else's)."""
    return get_object_or_404(UserWeight, pk=weight_id, user=request.user)


@login_required
def add_weight(request):
    if request.method == "POST":
        form = AdditionalWeight(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            messages.success(request, "Pomiar został dodany")
            return redirect("userPage")
    else:
        form = AdditionalWeight()

    return render(request, "main/weight_form.html", {"form": form})


@login_required
def edit_weight(request, weight_id):
    measurement = get_user_weight(request, weight_id)
    if request.method == "POST":
        form = AdditionalWeight(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            messages.success(request, "Pomiar został zmieniony")
            return redirect("userPage")
    else:
        form = AdditionalWeight(instance=measurement)

    return render(request, "main/weight_form.html", {"form": form, "measurement": measurement})


@login_required
@require_POST
def delete_weight(request, weight_id):
    get_user_weight(request, weight_id).delete()
    messages.success(request, "Pomiar został usunięty")
    return redirect("userPage")
