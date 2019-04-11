# Generated by Django 2.1.2 on 2018-10-09 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcmappv2', '0002_auto_20180909_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_title', models.CharField(max_length=50, verbose_name='Event title')),
                ('activity_date', models.DateField(verbose_name='Event date')),
                ('activity_venue', models.CharField(max_length=100, verbose_name='Event location')),
                ('activity_description', models.CharField(max_length=500, verbose_name='Event description')),
                ('activity_link_fb', models.URLField(blank=True, null=True, verbose_name='FB URL')),
                ('activity_link_ig', models.URLField(blank=True, null=True, verbose_name='IG URL')),
                ('activity_create_date', models.DateTimeField()),
                ('activity_image', models.FileField(upload_to='static/images', verbose_name='Upload image')),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'ordering': ['-activity_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['member_name']},
        ),
        migrations.AlterField(
            model_name='member',
            name='member_email',
            field=models.EmailField(max_length=200, unique=True, verbose_name='Email Address'),
        ),
    ]
