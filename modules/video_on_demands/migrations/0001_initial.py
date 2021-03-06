# Generated by Django 3.2.7 on 2022-03-07 13:01

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import modules.video_on_demands.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyFocus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Body Focus',
                'verbose_name_plural': 'Body Focus',
            },
        ),
        migrations.CreateModel(
            name='EquipmentRequired',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExampleVoD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(blank=True, upload_to=modules.video_on_demands.models.videos_thumb_location)),
                ('media_file', models.FileField(upload_to=modules.video_on_demands.models.videos_file_location)),
                ('about_video', models.TextField(blank=True, default='', max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Example Videos',
            },
        ),
        migrations.CreateModel(
            name='Intensity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkillLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('period', models.CharField(choices=[('days', 'Days'), ('months', 'MOnths')], default='days', max_length=30, verbose_name='Subscription period')),
                ('period_value', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('includes', models.TextField()),
                ('total_videos', models.PositiveIntegerField(default=0, verbose_name='No. Of videos')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'USD $'), ('EUR', 'EUR ???')], default='USD', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(currency_choices=[('USD', 'USD $'), ('EUR', 'EUR ???')], decimal_places=2, default_currency='USD', max_digits=10, null=True)),
                ('created_by', models.PositiveBigIntegerField(default=0, verbose_name='User Id')),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Video or Series name', max_length=200)),
                ('language', models.PositiveBigIntegerField(default=0)),
                ('about_video', models.TextField(default='', max_length=150)),
                ('additional_info', models.TextField(blank=True, default='', max_length=150)),
                ('is_series', models.BooleanField(default=False)),
                ('created_by', models.PositiveBigIntegerField(default=0, verbose_name='Created By User Id')),
                ('visible_to_user', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('draft', models.BooleanField(default=False)),
                ('body_focus', models.ManyToManyField(blank=True, to='video_on_demands.BodyFocus')),
                ('intensity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_on_demands.intensity')),
                ('required_equipments', models.ManyToManyField(blank=True, to='video_on_demands.EquipmentRequired')),
                ('skill_level', models.ManyToManyField(blank=True, to='video_on_demands.SkillLevel')),
                ('subscription', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_on_demands.videosubscription')),
                ('workout_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_on_demands.workouttype')),
            ],
            options={
                'verbose_name': 'Videos',
                'verbose_name_plural': 'Videos and Series',
            },
        ),
        migrations.CreateModel(
            name='UserVideoSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribed_user', models.PositiveBigIntegerField(default=0, verbose_name='User Id')),
                ('video_subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video_on_demands.videosubscription')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesEpisodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Episodes name', max_length=200)),
                ('about_video', models.TextField(default='', max_length=150)),
                ('additional_info', models.TextField(blank=True, default='', max_length=150)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('body_focus', models.ManyToManyField(blank=True, to='video_on_demands.BodyFocus')),
                ('intensity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_on_demands.intensity')),
                ('required_equipments', models.ManyToManyField(blank=True, to='video_on_demands.EquipmentRequired')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video_on_demands.videos')),
                ('skill_level', models.ManyToManyField(blank=True, to='video_on_demands.SkillLevel')),
                ('workout_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_on_demands.workouttype')),
            ],
            options={
                'verbose_name': 'Episodes',
                'verbose_name_plural': 'Episodes',
            },
        ),
        migrations.CreateModel(
            name='EpisodesMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(upload_to=modules.video_on_demands.models.episodes_file_location)),
                ('content_name', models.CharField(max_length=100)),
                ('media_type', models.CharField(max_length=20)),
                ('duration', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to=modules.video_on_demands.models.videos_thumb_location)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_on_demands.seriesepisodes')),
            ],
            options={
                'verbose_name': 'Series Episodes Media',
                'verbose_name_plural': 'Series Episodes Media',
            },
        ),
        migrations.CreateModel(
            name='CommonMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(upload_to=modules.video_on_demands.models.videos_file_location)),
                ('content_name', models.CharField(max_length=100)),
                ('media_type', models.CharField(max_length=20)),
                ('duration', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to=modules.video_on_demands.models.videos_thumb_location)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='video_on_demands.videos')),
            ],
            options={
                'verbose_name': 'Video, Series & Photo',
                'verbose_name_plural': 'Video, Photo & Series',
            },
        ),
    ]
