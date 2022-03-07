import pdb
from django.db import models
from gymstudio.models import Language, User, Currency
from modules.video_on_demands.models import WorkoutType, Intensity, SkillLevel, EquipmentRequired, BodyFocus
from djmoney.models.fields import MoneyField
from datetime import datetime
import time, os
from django.conf import settings

def classes_file_location(instance, filename):
    return '/'.join(['classes','uploads', str(instance.id), str(int(time.time())), filename])

def classes_thumb_location(instance, filename, *args, **kwargs):
    return '/'.join(['classes','uploads', str(instance.id), str(int(time.time())), filename[0]])

class ClassTemplate(models.Model):
    class Meta:
        verbose_name = 'Class Template'
        verbose_name_plural = 'Class Templates'
        
    name = models.CharField(max_length=200, help_text='Class Template Name')
    # language = models.IntegerField(Language, null=True, blank=True)
    language = models.PositiveBigIntegerField(default=0, blank=False)
    intensity = models.PositiveBigIntegerField(default=0, blank=True)
    # language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    # intensity = models.ForeignKey(Intensity, on_delete=models.SET_NULL, null=True, blank=True)
    subscriber_limit = models.IntegerField(blank=True)
    duration = models.IntegerField(blank=True)
    skill_level = models.ManyToManyField(SkillLevel, blank=True)
    required_equipments = models.ManyToManyField(EquipmentRequired, blank=True)
    body_focus = models.ManyToManyField(BodyFocus, blank=True)
    about_class = models.TextField(blank=True, default="", max_length=150)
    additional_info = models.TextField(blank=True, default="", max_length=150)
    user_id = models.PositiveBigIntegerField('Created By User Id', default=0)
    # currency = models.IntegerField(Currency, null=True, blank=True)
    price = models.IntegerField(blank=True, default='')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CommonMedia(models.Model):
    class Meta:
        verbose_name = 'Video, Series & Photo'
        verbose_name_plural = 'Video, Photo & Series'
    media_file = models.FileField(upload_to=classes_file_location)
    classtemplate = models.ForeignKey(ClassTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    content_name = models.CharField(max_length=100)
    media_type = models.CharField(max_length=20)
    duration = models.CharField(max_length=20, blank=True, null=True, default='')
    thumbnail = models.ImageField(upload_to=classes_thumb_location, blank=True)
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