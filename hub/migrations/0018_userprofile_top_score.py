# Generated by Django 5.1.4 on 2025-02-16 00:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0017_quizmodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='top_score',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hub.quizmodel'),
        ),
    ]
