from django.db import models
from exercises.models import Exercises
from reg_log.models import User



class TrainingPlans(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True)
    exercises = models.ManyToManyField(Exercises)
    
    def __str__(self):
        return self.name

class CustomPlans(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User)
    description = models.TextField(max_length=500, null=True)
    exercises = models.ManyToManyField(Exercises)
    
    def __str__(self):
        return self.name
