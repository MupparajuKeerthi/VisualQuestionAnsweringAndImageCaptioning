# Generated by Django 5.1 on 2025-03-02 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0005_detectionresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaptionPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_image_url', models.URLField(verbose_name='Uploaded Image URL')),
                ('actual_captions', models.JSONField(verbose_name='Actual Captions')),
                ('predicted_caption', models.CharField(max_length=500, verbose_name='Predicted Caption')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp of Caption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='captions', to='userapp.user', verbose_name='User')),
            ],
        ),
    ]
