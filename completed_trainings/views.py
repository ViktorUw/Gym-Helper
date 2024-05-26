from django.shortcuts import render
from itertools import chain


from training_plans.models import TrainingPlans, CustomPlans

def completed_trainings(request):
   
    return render(request, 'completed_trainings/completed_trainings.html')

def ct_create_training(request, selected_plan):
    selected_plan = selected_plan
    training_plans_count = TrainingPlans.objects.count()
    custom_plans_count = CustomPlans.objects.filter(user=request.user).count()
    trainings_plans = TrainingPlans.objects.all()
    custom_plans = CustomPlans.objects.filter(user=request.user)
    all_plans = chain(trainings_plans, custom_plans)
    size = custom_plans_count + training_plans_count
    # all_plans = trainings_plans | custom_plans

    content = {
        'selected_plan' : selected_plan,
        'all_plans' : all_plans,
        'size' : size,
        # 'custom_plans' : custom_plans,
        # 'trainings_plans' : trainings_plans,
    }

    return render(request, 'completed_trainings/ct_create_training.html', content)