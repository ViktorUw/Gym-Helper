from django.db import models

# Create your models here.

class userId_exerciseId(models.Model):
    user = models.ForeignKey('reg_log.User', on_delete=models.CASCADE)
    exercise = models.ForeignKey('exercises.Exercises', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.exercise}'