# Generated by Django 5.2.3 on 2025-07-15 05:42

import django.core.validators
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_egasp_data_retested_mic'),
    ]

    operations = [
        migrations.AddField(
            model_name='egasp_data',
            name='Date_Accomplished_Val',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='egasp_data',
            name='Val_contact',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AddField(
            model_name='egasp_data',
            name='Val_email',
            field=models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AddField(
            model_name='egasp_data',
            name='Validator',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
