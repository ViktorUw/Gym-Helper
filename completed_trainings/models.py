from django.db import models

from training_plans.models import TrainingPlans, CustomPlans
from exercises.models import Exercises
from reg_log.models import User
class CompletedTraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    training_plan = models.ForeignKey(TrainingPlans, on_delete=models.CASCADE, blank=True, null=True)
    custom_plan = models.ForeignKey(CustomPlans, on_delete=models.CASCADE, blank=True, null=True)
    exercises = models.ManyToManyField(Exercises)
    series = models.IntegerField()
    repetitions = models.IntegerField()
    weight = models.FloatField()

    
    def __str__(self):
        return f'{self.name} - {self.date} - {self.user}'
    
class Completed_Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    training_plan = models.ForeignKey(TrainingPlans, on_delete=models.CASCADE, blank=True, null=True)
    custom_plan = models.ForeignKey(CustomPlans, on_delete=models.CASCADE, blank=True, null=True)

    
    def __str__(self):
        return f'{self.name} - {self.date} - {self.user}'
    
class CompletedExercise(models.Model):
    training = models.ForeignKey(Completed_Training, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE, blank=True, null=True)
    series = models.IntegerField()
    repetitions = models.IntegerField()
    weight = models.FloatField()
