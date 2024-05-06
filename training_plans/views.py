from django.shortcuts import render
from .models import TrainingPlans, CustomPlans
from reg_log.models import User




def training_plans(request):
    training_plans = TrainingPlans.objects.all()
    custom_plans = CustomPlans.objects.filter(user=request.user)
    content = {
        'custom_plans' : custom_plans,
        'training_plans' : training_plans,

    }

    return render(request, 'training_plans/training_plans.html', content)

def training_plan(request, training_plan_id):
    training_plan = TrainingPlans.objects.get(pk=training_plan_id)

    context = {
        'training_plan': training_plan,
    }
    return render(request, 'training_plans/training_plan.html', context)
    
# def custom_plans(request):
#     custom_plans = CustomPlans.objects.all()
#     content = {
#         'custom_plans' : custom_plans
#     }
#     return render(request, 'training_plans/custom_plans.html', content)
