# Generated by Django 5.0.1 on 2025-02-08 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='original_images/')),
                ('enhanced_image', models.ImageField(blank=True, null=True, upload_to='enhanced_images/')),
                ('pixel_difference', models.FloatField(default=0.0)),
                ('differing_pixels', models.IntegerField(default=0)),
                ('total_pixels', models.IntegerField(default=0)),
            ],
        ),
    ]
