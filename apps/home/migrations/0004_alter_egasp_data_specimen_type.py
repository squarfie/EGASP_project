# Generated by Django 5.2.3 on 2025-07-03 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_egasp_data_growth_span'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egasp_data',
            name='Specimen_Type',
            field=models.CharField(choices=[('n/a', 'n/a'), ('Genital Male Urethral', 'Genital Male Urethral'), ('Female Cervical', 'Female Cervical'), ('Pharynx', 'Pharynx'), ('Rectum', 'Rectum'), ('Other', 'Other')], default='Genital Male Urethral', max_length=100),
        ),
    ]
