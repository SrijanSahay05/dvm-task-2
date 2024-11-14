# Generated by Django 5.1.3 on 2024-11-12 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('passenger', 'Passenger'), ('railwaystaff', 'Railway Staff'), ('admin', 'Admin')], default='passenger', max_length=20),
        ),
    ]