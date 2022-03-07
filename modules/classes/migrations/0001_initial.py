# Generated by Django 3.2.7 on 2022-03-07 13:01

from django.db import migrations, models
import django.db.models.deletion
import modules.classes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('video_on_demands', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Class Template Name', max_length=200)),
                ('language', models.PositiveBigIntegerField(default=0)),
                ('intensity', models.PositiveBigIntegerField(blank=True, default=0)),
                ('subscriber_limit', models.IntegerField(blank=True)),
                ('duration', models.IntegerField(blank=True)),
                ('skill_level', models.PositiveBigIntegerField(blank=True, default=0)),
                ('about_class', models.TextField(blank=True, default='', max_length=150)),
                ('additional_info', models.TextField(blank=True, default='', max_length=150)),
                ('user_id', models.PositiveBigIntegerField(default=0, verbose_name='Created By User Id')),
                ('price', models.IntegerField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('body_focus', models.ManyToManyField(blank=True, to='video_on_demands.BodyFocus')),
                ('required_equipments', models.ManyToManyField(blank=True, to='video_on_demands.EquipmentRequired')),
            ],
            options={
                'verbose_name': 'Class Template',
                'verbose_name_plural': 'Class Templates',
            },
        ),
        migrations.CreateModel(
            name='CommonMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(upload_to=modules.classes.models.classes_file_location)),
                ('content_name', models.CharField(max_length=100)),
                ('media_type', models.CharField(max_length=20)),
                ('duration', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to=modules.classes.models.classes_thumb_location)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('classtemplate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.classtemplate')),
            ],
            options={
                'verbose_name': 'Video, Series & Photo',
                'verbose_name_plural': 'Video, Photo & Series',
            },
        ),
    ]
