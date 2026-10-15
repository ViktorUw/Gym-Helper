from django.shortcuts import render
from reg_log.models import UserWeight

import matplotlib
matplotlib.use('Agg')  # render to images only; GUI backends break in server threads
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def index(request):
    return render(request, 'main/index.html')

def user_info(request):
    weight = UserWeight.objects.filter(user=request.user)
    
    weight = list(weight)

    if len(weight) == 0:
        last_weight = None
    else:
        last_weight = weight[-1]
    
    # Colours match main/static/main/css/style.css (dark theme, yellow accent)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot([w.date for w in weight], [w.weight for w in weight],
            color='#f2b705', linewidth=2.5, marker='o', markersize=5)
    ax.set_ylabel('kg', color='#9ba1a9')
    ax.tick_params(colors='#9ba1a9')
    ax.grid(axis='y', color='#383c43', linewidth=0.8)
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)
    ax.spines['bottom'].set_color('#383c43')
    fig.autofmt_xdate()
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png', transparent=True, dpi=150)
    plt.close(fig)
    buf.seek(0)

    image_png = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'main/user.html', {'last_weight': last_weight, 'weight' : weight, 'graph' : image_png})




    