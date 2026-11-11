from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from reg_log.models import UserWeight

from .charts import line_chart


@login_required
def index(request):
    return render(request, 'main/index.html')

@login_required
def user_info(request):
    weight = UserWeight.objects.filter(user=request.user)

    weight = list(weight)

    if len(weight) == 0:
        last_weight = None
    else:
        last_weight = weight[-1]

    graph = line_chart([w.date for w in weight], [w.weight for w in weight])

    return render(request, 'main/user.html', {'last_weight': last_weight, 'weight' : weight, 'graph' : graph})
