import pdb
from django.db import models
from djmoney.models.fields import MoneyField
import time, os
from gymstudio.models import Language
from django.conf import settings
from django.core.validators import FileExtensionValidator
# Create video subscription related models here.
def videos_file_location(instance, filename):
    return '/'.join(['videos','uploads', str(instance.id), str(int(time.time())), filename])

def videos_thumb_location(instance, filename, *args, **kwargs):
    return '/'.join(['videos','uploads', str(instance.id), str(int(time.time())), filename[0]])

def episodes_file_location(instance, filename):
    return '/'.join(['episodes','uploads', str(instance.id), str(int(time.time())), filename])

class VideoSubscription(models.Model):
    SUBSCRIPTION_PERIODS = (
        ('days', 'Days'),
        ('months', 'MOnths'),
    )
    
    CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €')]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    period = models.CharField('Subscription period',max_length=30, choices=SUBSCRIPTION_PERIODS, default='days')
    period_value = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    includes = models.TextField()
    total_videos = models.PositiveIntegerField('No. Of videos',default=0)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', currency_choices=CURRENCY_CHOICES, null=True)
    created_by = models.PositiveBigIntegerField('User Id', default=0)
    def __str__(self):
        return self.name
    
    @property
    def videos(self):
        return self.videos_set.all()
    
    @property
    def users(self):
        return self.uservideosubscription_set.all()

    @property
    def can_delete(self):
        return not self.videos.exists() and not self.users.exists()
    
class UserVideoSubscription(models.Model):
    subscribed_user = models.PositiveBigIntegerField('User Id', default=0)
    video_subscription = models.ForeignKey(VideoSubscription, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)

class WorkoutType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Intensity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class SkillLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class EquipmentRequired(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class BodyFocus(models.Model):
    class Meta:
        verbose_name = 'Body Focus'
        verbose_name_plural = 'Body Focus'
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Videos(models.Model):
    class Meta:
        verbose_name = 'Videos'
        verbose_name_plural = 'Videos and Series'
        
    name = models.CharField(max_length=200, help_text='Video or Series name')
    language = models.PositiveBigIntegerField(default=0, blank=False)
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.SET_NULL, null=True, blank=True)
    intensity = models.ForeignKey(Intensity, on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey(VideoSubscription, on_delete=models.SET_NULL, null=True, blank=True)
    skill_level = models.ManyToManyField(SkillLevel, blank=True)
    required_equipments = models.ManyToManyField(EquipmentRequired, blank=True)
    body_focus = models.ManyToManyField(BodyFocus, blank=True)
    about_video = models.TextField(default="", max_length=150)
    additional_info = models.TextField(blank=True, default="", max_length=150)
    is_series = models.BooleanField(default=False)
    created_by = models.PositiveBigIntegerField('Created By User Id', default=0)
    visible_to_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    @property
    def video(self):
        common_media = self.commonmedia_set.filter(content_name='Video', media_type__contains='video').last()
        return common_media
    
class CommonMedia(models.Model):
    class Meta:
        verbose_name = 'Video, Series & Photo'
        verbose_name_plural = 'Video, Photo & Series'
    media_file = models.FileField(upload_to=videos_file_location)
    video = models.ForeignKey(Videos, on_delete=models.SET_NULL, null=True, blank=True)
    content_name = models.CharField(max_length=100)
    media_type = models.CharField(max_length=20)
    duration = models.CharField(max_length=20, blank=True, null=True, default='')
    thumbnail = models.ImageField(upload_to=videos_thumb_location, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content_name
        
    @property
    def has_thumb(self):
        if self.thumbnail:
            return True
        return False
    
    @property
    def get_thumbnail(self):
        if self.has_thumb:
            return self.thumbnail.url
        return '/static/images/videoPreview.png'
    
    @property
    def get_image(self):
        if self.media_file:
            return self.media_file.url
        return '/static/images/no-image.svg'
    
    @property
    def get_filename(self):
        if self.media_file:
            return os.path.basename(self.media_file.name)
        return ''
    
    @property
    def is_video(self):
        return self.media_type in settings.VIDEO_TYPES
    
    @property
    def is_image(self):
        return self.media_type in settings.IMAGE_TYPES
    
class SeriesEpisodes(models.Model):
    class Meta:
        verbose_name = 'Episodes'
        verbose_name_plural = 'Episodes'
        
    name = models.CharField(max_length=200, help_text='Episodes name')
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.SET_NULL, null=True, blank=True)
    intensity = models.ForeignKey(Intensity, on_delete=models.SET_NULL, null=True, blank=True)
    skill_level = models.ManyToManyField(SkillLevel, blank=True)
    required_equipments = models.ManyToManyField(EquipmentRequired, blank=True)
    body_focus = models.ManyToManyField(BodyFocus, blank=True)
    about_video = models.TextField(default="", max_length=150)
    additional_info = models.TextField(blank=True, default="", max_length=150)
    series = models.ForeignKey(Videos, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    @property
    def video(self):
        common_media = self.episodesmedia_set.filter(content_name='Video', media_type__contains='video').last()
        return common_media

class EpisodesMedia(models.Model):
    class Meta:
        verbose_name = 'Series Episodes Media'
        verbose_name_plural = 'Series Episodes Media'
    media_file = models.FileField(upload_to=episodes_file_location)
    series = models.ForeignKey(SeriesEpisodes, on_delete=models.SET_NULL, null=True, blank=True)
    content_name = models.CharField(max_length=100)
    media_type = models.CharField(max_length=20)
    duration = models.CharField(max_length=20, blank=True, null=True, default='')
    thumbnail = models.ImageField(upload_to=videos_thumb_location, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content_name
    
    @property
    def has_thumb(self):
        if self.thumbnail:
            return True
        return False
    
    @property
    def get_thumbnail(self):
        if self.has_thumb:
            return self.thumbnail.url
        return '/static/images/videoPreview.png'
    
    @property
    def get_image(self):
        if self.media_file:
            return self.media_file.url
        return '/static/images/no-image.svg'
    
    @property
    def get_filename(self):
        if self.media_file:
            return os.path.basename(self.media_file.name)
        return ''
    
    @property
    def is_video(self):
        return self.media_type in settings.VIDEO_TYPES
    
    @property
    def is_image(self):
        return self.media_type in settings.IMAGE_TYPES
    
class ExampleVoD(models.Model):
    class Meta:
        verbose_name_plural = 'Example Videos'

    thumbnail = models.ImageField(upload_to=videos_thumb_location, blank=True)
    media_file = models.FileField(upload_to=videos_file_location)
    about_video = models.TextField(blank=True, default="", max_length=150)
    
    @property
    def has_thumb(self):
        if self.thumbnail:
            return True
        return False
    
    @property
    def get_thumbnail(self):
        if self.has_thumb:
            return self.thumbnail.url
        return ''

from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import create_thumbnail
@receiver(post_save, sender=ExampleVoD)
def create_thumbnail_call(sender, instance, **kwargs):
    create_thumbnail(instance)