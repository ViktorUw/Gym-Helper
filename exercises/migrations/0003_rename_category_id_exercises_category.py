# Generated by Django 5.0.3 on 2024-04-08 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_rename_exercise_exercises'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercises',
            old_name='category_id',
            new_name='category',
        ),
    ]