# Generated by Django 5.0.3 on 2024-06-02 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('completed_trainings', '0003_remove_completed_training_exercises_and_more'),
        ('exercises', '0007_delete_trainingplans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='completed_training',
            name='exercises',
        ),
        migrations.RemoveField(
            model_name='completed_training',
            name='repetitions',
        ),
        migrations.RemoveField(
            model_name='completed_training',
            name='series',
        ),
        migrations.RemoveField(
            model_name='completed_training',
            name='weight',
        ),
        migrations.CreateModel(
            name='CompletedExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.IntegerField()),
                ('repetitions', models.IntegerField()),
                ('weight', models.FloatField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.exercises')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='completed_trainings.completedtraining')),
            ],
        ),
    ]