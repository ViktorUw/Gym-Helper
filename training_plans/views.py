from django.shortcuts import render
from .models import TrainingPlans



def training_plans(request):
    training_plans = TrainingPlans.objects.all()
    content = {
        'training_plans' : training_plans
    }

    return render(request, 'training_plans/training_plans.html', content)

def training_plan(request, training_plan_id):
    training_plan = TrainingPlans.objects.get(pk=training_plan_id)
    context = {
        'training_plan': training_plan,
    }
    return render(request, 'training_plans/training_plan.html', context)
    