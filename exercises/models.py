from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.name

    @property
    def plate(self):
        """Colour slot 1-6 used by the templates (CSS classes plate-1 ... plate-6)."""
        return (self.pk - 1) % 6 + 1


class Exercises(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(max_length=500, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    video = models.CharField(max_length=500, null=True)
    
    def __str__(self):
        return self.name
    
