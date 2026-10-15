from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CreateCustomPlanForm
from .models import CustomPlans, TrainingPlans


def training_plans(request):
    training_plans = TrainingPlans.objects.all()
    custom_plans = CustomPlans.objects.filter(user=request.user)
    content = {
        "custom_plans": custom_plans,
        "training_plans": training_plans,
    }

    return render(request, "training_plans/training_plans.html", content)


def training_plan(request, training_plan_id):
    training_plan = TrainingPlans.objects.get(pk=training_plan_id)

    context = {
        "training_plan": training_plan,
    }
    return render(request, "training_plans/training_plan.html", context)


def custom_plan(request, custom_plan_id):
    custom_plan = CustomPlans.objects.get(pk=custom_plan_id)
    content = {
        "custom_plan": custom_plan,
    }
    return render(request, "training_plans/custom_plan.html", content)


def create_plan(request):
    if request.method == "POST":
        form = CreateCustomPlanForm(request.POST)
        if form.is_valid():
            custom_plan = form.save(commit=False)
            custom_plan.save()
            custom_plan.user.set([request.user])
            form.save_m2m()
            messages.success(request, "Plan was created sucfully!")

            return redirect("/training/")
    else:
        form = CreateCustomPlanForm()

    context = {"form": form}
    return render(request, "training_plans/create_plan.html", context)


@require_POST
def delete_plan(request, custom_plan_id):
    custom_plan = get_object_or_404(CustomPlans, pk=custom_plan_id, user=request.user)
    custom_plan.delete()
    messages.success(request, "Plan został usunięty!")
    return redirect("trainingPlansPage")
