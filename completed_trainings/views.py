from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from exercises.models import Exercises
from training_plans.models import CustomPlans, TrainingPlans

from .forms import AddExerciseForm, AdditionalWeight, TrainingPlanForm
from .models import Completed_Training, CompletedExercise


def get_user_training(request, training_id):
    """The user's own training, or 404 (also for someone else's training)."""
    return get_object_or_404(Completed_Training, id=training_id, user=request.user)


def training_exercises(training):
    """Exercises of the training's plan; if the plan was deleted, the ones with logged sets."""
    plan = training.training_plan or training.custom_plan
    if plan:
        return plan.exercises.all()
    return Exercises.objects.filter(completedexercise__training=training).distinct()


# FOR COMPLETED TRAININGS
@login_required
def completed_trainings(request):
    completed_trainings = Completed_Training.objects.filter(user=request.user)
    return render(
        request,
        "completed_trainings/completed_trainings.html",
        {"completed_trainings": completed_trainings},
    )


# FOR ADDING WEIGHT
@login_required
def add_weight(request):
    form = AdditionalWeight()
    if request.method == "POST":
        form = AdditionalWeight(request.POST)
        if form.is_valid():
            weight_instance = form.save(commit=False)
            weight_instance.user = request.user
            weight_instance.save()
            return redirect("choseTrainingPlanPage")
    else:
        form = AdditionalWeight()

    return render(request, "completed_trainings/add_weight.html", {"form": form})


@login_required
def chose_training_plan(request):
    if request.method == "POST":
        form_for_plans = TrainingPlanForm(request.POST, user=request.user)
        if form_for_plans.is_valid():
            # Value is "tp-<id>" for a ready plan or "cp-<id>" for a custom plan,
            # because both tables number their plans independently
            kind, plan_id = form_for_plans.cleaned_data["plan"].split("-")
            training = form_for_plans.save(commit=False)
            training.user = request.user
            if kind == "tp":
                training.training_plan = get_object_or_404(TrainingPlans, id=plan_id)
            else:
                training.custom_plan = get_object_or_404(
                    CustomPlans, id=plan_id, user=request.user
                )
            training.save()
            return redirect("trainingsPage")
    else:
        form_for_plans = TrainingPlanForm(user=request.user)

    return render(
        request,
        "completed_trainings/chose_training_plan.html",
        {"form_for_plans": form_for_plans},
    )


@login_required
def ct_create_training(request, training_id):
    training = get_user_training(request, training_id)
    training_name = training.training_name
    plan_id = training.training_plan_id or training.custom_plan_id
    exercises = training_exercises(training)

    completed_exercises = CompletedExercise.objects.filter(training=training)
    # Sets grouped per exercise, so the template can number them 1, 2, 3... for each exercise
    exercise_sets = [
        (ex, [ce for ce in completed_exercises if ce.exercise_id == ex.id])
        for ex in exercises
    ]

    # return HttpResponse(completed_exercises[0])
    content = {
        "training_name": training_name,
        "plan_id": plan_id,
        "exercises": exercises,
        "training_id": training_id,
        "completed_exercises": completed_exercises,
        "exercise_sets": exercise_sets,
    }

    return render(request, "completed_trainings/ct_create_training.html", content)


@login_required
def do_series(request, training_id):
    training = get_user_training(request, training_id)
    # Without a plan (it was deleted) any exercise can be logged
    exercises = (
        training_exercises(training)
        if (training.training_plan_id or training.custom_plan_id)
        else Exercises.objects.all()
    )

    if request.method == "POST":
        add_exercise_form = AddExerciseForm(request.POST, exercises=exercises)
        if add_exercise_form.is_valid():
            exercise_instance = add_exercise_form.save(commit=False)
            exercise_instance.exercise = add_exercise_form.cleaned_data["exercise"]
            exercise_instance.training = training
            exercise_instance.save()
            return redirect("ct_create_trainingsPage", training_id=training_id)
    else:
        add_exercise_form = AddExerciseForm(exercises=exercises)

    return render(
        request,
        "completed_trainings/do_series.html",
        {"add_exercise_form": add_exercise_form},
    )


@login_required
@require_POST
def delete_training(request, training_id):
    training = get_object_or_404(Completed_Training, id=training_id, user=request.user)
    training.delete()
    messages.success(request, "Trening został usunięty")
    return redirect("trainingsPage")
