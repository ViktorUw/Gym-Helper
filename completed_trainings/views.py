from django.shortcuts import render
from reg_log.models import UserWieght
from training_plans.models import TrainingPlans, CustomPlans
from itertools import chain
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date


# FOR COMPLETED TRAININGS
def completed_trainings(request):
    return render(request, 'completed_trainings/completed_trainings.html')


# DLA WYBORU PLANU TRENINGU DO WYKONANIA
def chose_training_plan(request):
    #ŁADUJEMY WSZYTKIE DOSTĘPNE PLANU TRENINGOWE
    training_plans = TrainingPlans.objects.all()
    custom_plans = CustomPlans.objects.filter(user=request.user)
    all_plans = list(chain(training_plans, custom_plans))
    content = {
        'all_plans' : all_plans,
    }
    return render(request, 'completed_trainings/chose_training_plan.html', content)

# ОПРАЦЮВАННЯ ВИБОРУ ПЛАНУ ТРЕНУВАНЬ
# return HttpResponse(training_plan_id)
def process_plan(request):
    training_plans = TrainingPlans.objects.all()
    custom_plans = CustomPlans.objects.filter(user=request.user)
    if request.method == 'POST' and 'training_plan' in request.POST:
        training_plan_id = request.POST['training_plan']
        training_name = request.POST['training_name']        
        weight = float(request.POST['weight'])
        UserWieght.objects.create(user=request.user, weight=weight, date=date.today())
        if TrainingPlans.objects.filter(id=training_plan_id).exists() and len(training_name) != 0 and weight > 0:
            exersises = training_plans.get(id=training_plan_id).exercises.all()
            return render(request, 'completed_trainings/ct_create_training.html', {'exersises': exersises, 'training_name': training_name})
        elif CustomPlans.objects.filter(id=training_plan_id).exists() and len(training_name) != 0 and weight > 0:
            exersises = custom_plans.get(id=training_plan_id).exercises.all()
            return render(request, 'completed_trainings/ct_create_training.html', {'exersises': exersises, 'training_name': training_name})
        else:
            return HttpResponseRedirect('/completed_trainings/chose_training_plan/')
    else:
        return HttpResponseRedirect('/completed_trainings/chose_training_plan/')
        # return render(request, 'completed_trainings/chose_training_plan.html', {'all_plans': all_plans})
        
def ct_create_training(request):
    return render(request, 'completed_trainings/ct_create_training.html')