# Generated by Django 5.0.12 on 2025-03-16 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='breakpointstable',
            name='Operator',
        ),
    ]
