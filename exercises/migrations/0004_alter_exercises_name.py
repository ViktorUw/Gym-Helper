# Generated by Django 5.0.3 on 2024-04-09 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0003_rename_category_id_exercises_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercises',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]