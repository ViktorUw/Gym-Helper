from django.shortcuts import render, redirect
from reg_log.models import UserWeight
from training_plans.models import TrainingPlans, CustomPlans
from itertools import chain
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from .forms import AdditionalWeight, TrainingPlanForm

# FOR COMPLETED TRAININGS
def completed_trainings(request):
    return render(request, 'completed_trainings/completed_trainings.html')


def add_weight(request):
    form = AdditionalWeight()
    if request.method == 'POST':
        form = AdditionalWeight(request.POST)
        if form.is_valid():
            weight_instance = form.save(commit=False)
            weight_instance.user = request.user
            weight_instance.save()
            return redirect('choseTrainingPlanPage')
            return render(request, 'completed_trainings/chose_training_plan.html', {'form': form})
    else:
        form = AdditionalWeight()
    
    return render(request, 'completed_trainings/add_weight.html', {'form': form})

def chose_training_plan(request):
    form_for_plans = TrainingPlanForm()
    if request.method == 'POST':
        form_for_plans = TrainingPlanForm(request.POST, user=request.user)
        if form_for_plans.is_valid():
            plan_id = form_for_plans.cleaned_data['plan']
            if TrainingPlans.objects.filter(id=plan_id).exists():
                training_plan_exercises = TrainingPlans.objects.get(id=plan_id).exercises.all()
                content = {
                    'id': plan_id,
                    'training_plan': training_plan_exercises,
                    'form_for_plans': form_for_plans,
                }        

                return render(request, 'completed_trainings/ct_create_training.html', content) 
            elif CustomPlans.objects.filter(id=plan_id).exists():
                custom_plans_exercises = CustomPlans.objects.get(id=plan_id).exercises.all()
                content = {
                    'id': plan_id,
                    'custom_plans': custom_plans_exercises,
                    'form_for_plans': form_for_plans,
                } 
                return render(request, 'completed_trainings/ct_create_trainings.html', content) 
    else:
        form_for_plans = TrainingPlanForm(user=request.user)
                
    return render(request, 'completed_trainings/chose_training_plan.html', {'form_for_plans': form_for_plans})
    
def ct_create_training(request):
    return render(request, 'completed_trainings/ct_create_training.html')
