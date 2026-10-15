from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render


from .models import Exercises, Category
from django.http import HttpResponse
# Create your views here.


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
    # description = exercise.description
    

    context = {
        "exercise": exercise,
        # 'exercise_id': exercise.pk, # 'exercise_id' is a key that will be used in the template to access the value 'exercise_id'
        # 'exercise_name': exercise.name,
        # 'exercise_description': exercise.description,
    }
    # return HttpResponse(f'<h1>{exercise.name}</h1><p>{exercise.description}</p>')
    return render(request, 'exercises/exercise.html', context)