from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import get_object_or_404, render

from completed_trainings.models import CompletedExercise
from main.charts import line_chart

from .models import Exercises, Category


@login_required
def exercises(request):
    category = Category.objects.all()
    exercises = Exercises.objects.all()
    content = {
        'category': category,
        'exercises': exercises
    }

    return render(request, 'exercises/exercises.html', content)

@login_required
def exercise(request, exercise_id):
    exercise = get_object_or_404(Exercises, pk=exercise_id)

    # Only the current user's sets of this exercise
    sets = CompletedExercise.objects.filter(exercise=exercise, training__user=request.user)
    best = sets.order_by("-weight", "-repetitions").first()
    # Heaviest set of each training day, oldest first
    per_day = list(
        sets.values("training__date")
        .annotate(top_weight=Max("weight"))
        .order_by("training__date")
    )
    # A chart needs at least two days to show a change
    chart = None
    if len(per_day) >= 2:
        chart = line_chart(
            [day["training__date"] for day in per_day],
            [day["top_weight"] for day in per_day],
        )

    context = {
        "exercise": exercise,
        "best": best,
        "sets_count": sets.count(),
        "days_count": len(per_day),
        "last_date": per_day[-1]["training__date"] if per_day else None,
        "chart": chart,
    }
    return render(request, 'exercises/exercise.html', context)
