# Generated by Django 5.1.4 on 2025-02-14 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0007_questionmodel_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionmodel',
            name='level',
        ),
        migrations.AddField(
            model_name='quizmodel',
            name='levels',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
