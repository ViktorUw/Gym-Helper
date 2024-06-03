# Generated by Django 5.0.3 on 2024-06-02 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('completed_trainings', '0001_initial'),
        ('exercises', '0007_delete_trainingplans'),
        ('training_plans', '0003_customplans_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Completed_Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('series', models.IntegerField()),
                ('repetitions', models.IntegerField()),
                ('weight', models.FloatField()),
                ('custom_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training_plans.customplans')),
                ('exercises', models.ManyToManyField(to='exercises.exercises')),
                ('training_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training_plans.trainingplans')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]