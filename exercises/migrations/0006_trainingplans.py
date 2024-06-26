# Generated by Django 5.0.3 on 2024-04-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_alter_exercises_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500, null=True)),
                ('exercises', models.ManyToManyField(to='exercises.exercises')),
            ],
        ),
    ]
