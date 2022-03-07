from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from .models import CommonMedia, Videos, SeriesEpisodes, ExampleVoD
from django_summernote.admin import SummernoteModelAdmin
from .forms import ExampleVodForm
models = apps.get_models()

class CommonMediaAdmin(admin.ModelAdmin):
    list_display = ['content_name', 'media_type', 'video', 'created_at']

class SeriesEpisodesContent(admin.StackedInline):
    model = SeriesEpisodes
    extra = 0
    
class MediaContent(admin.StackedInline):
    model = CommonMedia
    extra = 0
    
class VideoSeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_series', 'created_by', 'about_video', 'created_at']
    inlines = [SeriesEpisodesContent, MediaContent]

admin.site.register(Videos, VideoSeriesAdmin)
admin.site.register(CommonMedia, CommonMediaAdmin)

@admin.register(ExampleVoD)
class VideoAdmin(SummernoteModelAdmin):
   list_dispaly = ('get_filename', )
   readonly_fields = ('thumbnail',)
   summernote_fields = ('about_video',)
   form = ExampleVodForm
   
for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered as ex:
        pass