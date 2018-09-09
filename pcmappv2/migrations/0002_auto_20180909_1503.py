# Generated by Django 2.1 on 2018-09-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcmappv2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_model',
            field=models.CharField(choices=[('2008', '2008'), ('206', '206'), ('206 CC', '206 CC'), ('207 Sedan', '207 Sedan'), ('207 CC', '207 CC'), ('208', '208'), ('208 GTi', '208 GTi'), ('3008', '3008'), ('305', '305'), ('306', '306'), ('307', '307'), ('307 SW', '307 SW'), ('308', '308'), ('308 CC', '308 CC'), ('308 GT', '308 GT'), ('405', '405'), ('406', '406'), ('407', '407'), ('407 SW', '407 SW'), ('408', '408'), ('5008', '5008'), ('504', '504'), ('505', '505'), ('508', '508'), ('508 GT', '508 GT'), ('508 SW', '508 SW'), ('607', '607'), ('807', '807'), ('Partner', 'Partner'), ('RCZ', 'RCZ'), ('Traveller', 'Traveller')], max_length=20, verbose_name='Model'),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_status',
            field=models.BooleanField(default=True, verbose_name='Membership Status'),
        ),
    ]
