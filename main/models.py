from django.db import models

# Create your models here.

class userId_planID(models.Model):
    user = models.ForeignKey('reg_log.User', on_delete=models.CASCADE)
    plan = models.ForeignKey('training_plans.TrainingPlans', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.plan}'