from django.db import models
from exercises.models import Exercises



class TrainingPlans(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True)
    exercises = models.ManyToManyField(Exercises)
    
    def __str__(self):
        return self.name
