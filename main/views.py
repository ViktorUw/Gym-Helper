from django.shortcuts import render
from reg_log.models import UserWeight

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
    
    plt.figure(figsize=(10,5))
    plt.plot([w.date for w in weight], [w.weight for w in weight])
    plt.title('Postęp wagi')
    plt.xlabel('Data')
    plt.ylabel('Waga')
   
    buf = BytesIO()
    plt.savefig(buf, format='jpeg')
    buf.seek(0)
    
    image_jpeg = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'main/user.html', {'last_weight': last_weight, 'weight' : weight, 'graph' : image_jpeg})




    