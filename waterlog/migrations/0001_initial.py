# Generated by Django 5.0.4 on 2024-04-05 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WaterLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_name', models.CharField(max_length=100)),
                ('watered_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
