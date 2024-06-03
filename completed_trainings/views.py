from django.shortcuts import render, redirect
from reg_log.models import UserWeight
from training_plans.models import TrainingPlans, CustomPlans
from itertools import chain
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from .forms import AdditionalWeight, TrainingPlanForm
from .models import Completed_Training, CompletedExercise


# FOR COMPLETED TRAININGS
def completed_trainings(request):
    completed_trainings = Completed_Training.objects.filter(user=request.user)
    return render(request, 'completed_trainings/completed_trainings.html', {'completed_trainings': completed_trainings})

# FOR ADDING WEIGHT
def add_weight(request):
    form = AdditionalWeight()
    if request.method == 'POST':
        form = AdditionalWeight(request.POST)
        if form.is_valid():
            weight_instance = form.save(commit=False)
            weight_instance.user = request.user
            weight_instance.save()
            return redirect('choseTrainingPlanPage')
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
                
                form_for_plans_instance = form_for_plans.save(commit=False)
                form_for_plans_instance.user = request.user
                form_for_plans_instance.training_plan_id = plan_id
                form_for_plans_instance.save()

                training_plan_exercises = TrainingPlans.objects.get(id=plan_id).exercises.all()
                content = {
                    'id': plan_id,
                    'training_plan': training_plan_exercises,
                    'form_for_plans': form_for_plans,
                }        
                
                return redirect('trainingsPage')
                return render(request, 'completed_trainings/ct_create_training.html', content) 
            elif CustomPlans.objects.filter(id=plan_id).exists():
                form_for_plans_instance = form_for_plans.save(commit=False)
                form_for_plans_instance.user = request.user
                form_for_plans_instance.custom_plan_id = plan_id
                form_for_plans_instance.save()
               
                custom_plans_exercises = CustomPlans.objects.get(id=plan_id).exercises.all()
                content = {
                    'id': plan_id,
                    'custom_plans': custom_plans_exercises,
                    'form_for_plans': form_for_plans,
                } 
                return redirect('trainingsPage')
                return render(request, 'completed_trainings/ct_create_training.html', content) 
    else:
        form_for_plans = TrainingPlanForm(user=request.user)
                    
    return render(request, 'completed_trainings/chose_training_plan.html', {'form_for_plans': form_for_plans})
    
def ct_create_training(request, training_id):
    training_name = Completed_Training.objects.get(id=training_id).training_name
    plan_id = None
    if Completed_Training.objects.get(id=training_id).training_plan_id:
        plan_id = Completed_Training.objects.get(id=training_id).training_plan_id
        exercises = TrainingPlans.objects.get(id=plan_id).exercises.all()
        
    elif Completed_Training.objects.get(id=training_id).custom_plan_id:
        plan_id = Completed_Training.objects.get(id=training_id).custom_plan_id
        exercises = CustomPlans.objects.get(id=plan_id).exercises.all()
    content = {
        'training_name' : training_name,
        'plan_id' : plan_id,
        'exercises' : exercises,
    }
    return render(request, 'completed_trainings/ct_create_training.html', content)
    
    if TrainingPlans.objects.filter(id=training_id).exists():
        training_plan_exercises = TrainingPlans.objects.get(id=training_id).exercises.all()
        content = {
            'id': training_id,
            'training_plan': training_plan_exercises,
        }
        return render(request, 'completed_trainings/ct_create_training.html', content)
    elif CustomPlans.objects.filter(id=training_id).exists():
        custom_plans_exercises = CustomPlans.objects.get(id=training_id).exercises.all()
        content = {
            'id': training_id,
            'custom_plans': custom_plans_exercises,
        }
        return render(request, 'completed_trainings/ct_create_training.html', content)
    else:
        return HttpResponse('No such training plan')

def do_series(request):
    return render(request, 'completed_trainings/do_series.html')