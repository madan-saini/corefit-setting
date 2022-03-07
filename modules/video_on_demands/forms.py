import pdb
# from tkinter import Widget
from django import forms
from .models import ExampleVoD, EpisodesMedia, VideoSubscription, WorkoutType, Intensity, Videos, BodyFocus, EquipmentRequired, CommonMedia, SkillLevel, SeriesEpisodes
from djmoney.forms import MoneyField
from django.core.exceptions import ValidationError
import magic
from gymstudio.models import Language, User
from django.conf import settings
from .tasks import create_thumbnail, get_duration

def user_languages(user_id):
    try:
        user_langs = User.objects.get(id=user_id).languages.split(',')
        return tuple(Language.objects.filter(id__in=user_langs).values_list('id', 'name'))
    except:
        return ()
    
class VideoSubscriptionForm(forms.ModelForm):
    price = MoneyField(max_digits=10, currency_choices=VideoSubscription.CURRENCY_CHOICES, currency_widget=forms.Select(attrs={'class': 'form-control drop-down'}, choices=VideoSubscription.CURRENCY_CHOICES))
    class Meta:
        model = VideoSubscription
        fields = ['name', 'description', 'period_value', 'period', 'includes', 'price','created_by']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'maxlength': 100}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'includes': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'period': forms.HiddenInput(),
            'period_value': forms.NumberInput(attrs={'class': 'form-control only-number', 'required': True}),
            # 'total_videos': forms.NumberInput(attrs={'class': 'form-control only-number'}),
            'created_by': forms.HiddenInput()
        }
    def __init__(self, request, *args, **kwargs):
        instance = super(VideoSubscriptionForm, self).__init__(*args, **kwargs)
        if not instance:
            self.fields['period'].initial = 'days'
        self.fields['created_by'].initial = request.session.get('user_id')

class VideoSubscriptionUpdateForm(forms.ModelForm):
    price = MoneyField(max_digits=10, currency_choices=VideoSubscription.CURRENCY_CHOICES, currency_widget=forms.Select(attrs={'class': 'form-control drop-down'}, choices=VideoSubscription.CURRENCY_CHOICES))
    class Meta:
        model = VideoSubscription
        fields = ['name', 'description', 'period_value', 'period', 'includes', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'maxlength': 100}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'includes': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'period': forms.HiddenInput(),
            'period_value': forms.NumberInput(attrs={'class': 'form-control only-number', 'required': True}),
            # 'total_videos': forms.NumberInput(attrs={'class': 'form-control only-number'}),
        }
    def __init__(self, request, *args, **kwargs):
        instance = super(VideoSubscriptionUpdateForm, self).__init__(*args, **kwargs)
        self.request = request

class NewSeriesForm(forms.ModelForm):
    subscription = forms.ModelChoiceField(queryset=VideoSubscription.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))

    class Meta:
        model = Videos
        fields = ['name',
                    'language',
                    'subscription',
                    'about_video',
                    'created_by',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about_video': forms.Textarea(attrs={'class': 'form-control'}),
            'created_by': forms.HiddenInput(),
            'language': forms.Select(attrs={'class': 'form-control select-single', 'required': True})
        }
    
    def __init__(self, request, *args, **kwargs):
        super(NewSeriesForm, self).__init__(*args, **kwargs)
        self.request = request
        user = request.session.get('user_id', 0)
        self.fields['created_by'].initial = user
        self.fields['subscription'].queryset = VideoSubscription.objects.filter(created_by=user)
        self.fields['language'].widget.choices = user_languages(request.session.get('user_id'))
        
    def save(self, commit=True):
        instance = super(NewSeriesForm, self).save(commit=False)
        instance.is_series = True
        instance.draft = True
        
        if commit:
            instance.save()
            self.save_m2m()
            
        data = self.request.POST.dict()
        file_ids = [ value for key, value in data.items() if key.endswith('_file') and value]
        CommonMedia.objects.filter(id__in=file_ids).update(video = instance)
        return instance
    

class NewVideosForm(forms.ModelForm):
    required_equipments = forms.ModelMultipleChoiceField(queryset=EquipmentRequired.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    body_focus = forms.ModelMultipleChoiceField(queryset=BodyFocus.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    skill_level = forms.ModelMultipleChoiceField(queryset=SkillLevel.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    workout_type = forms.ModelChoiceField(queryset=WorkoutType.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))
    intensity = forms.ModelChoiceField(queryset=Intensity.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))
    subscription = forms.ModelChoiceField(queryset=VideoSubscription.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))

    class Meta:
        model = Videos
        fields = ['name',
                    'language',
                    'workout_type',
                    'intensity',
                    'skill_level',
                    'subscription',
                    'required_equipments',
                    'body_focus',
                    'about_video',
                    'additional_info',
                    'created_by',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about_video': forms.Textarea(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control'}),
            'created_by': forms.HiddenInput(),
            'language': forms.Select(attrs={'class': 'form-control select-single', 'required': True})
        }
    
    def __init__(self, request, *args, **kwargs):
        super(NewVideosForm, self).__init__(*args, **kwargs)
        self.request = request
        user = request.session.get('user_id', 0)
        self.fields['created_by'].initial = user
        self.fields['subscription'].queryset = VideoSubscription.objects.filter(created_by=user)
        self.fields['language'].widget.choices = user_languages(request.session.get('user_id'))
        
    def save(self, commit=True):
        instance = super(NewVideosForm, self).save(commit=False)
        instance.is_series = False
        instance.draft = False
        instance.visible_to_user = True
        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the video with required_equipments
           instance.required_equipments.clear()
           instance.required_equipments.add(*self.cleaned_data['required_equipments'])
           # This is where we actually link the video with body_focus
           instance.body_focus.clear()
           instance.body_focus.add(*self.cleaned_data['body_focus'])
           # This is where we actually link the video with skill_level
           instance.skill_level.clear()
           instance.skill_level.add(*self.cleaned_data['skill_level'])
        self.save_m2m = save_m2m
        
        if commit:
            instance.save()
            self.save_m2m()
            
        data = self.request.POST.dict()
        file_ids = [ value for key, value in data.items() if key.endswith('_file') and value]
        CommonMedia.objects.filter(id__in=file_ids).update(video = instance)
        return instance

class UpdateVideosForm(forms.ModelForm):
    required_equipments = forms.ModelMultipleChoiceField(queryset=EquipmentRequired.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    body_focus = forms.ModelMultipleChoiceField(queryset=BodyFocus.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    skill_level = forms.ModelMultipleChoiceField(queryset=SkillLevel.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    workout_type = forms.ModelChoiceField(queryset=WorkoutType.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))
    intensity = forms.ModelChoiceField(queryset=Intensity.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))
    subscription = forms.ModelChoiceField(queryset=VideoSubscription.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))

    class Meta:
        model = Videos
        fields = ['name',
                    'language',
                    'workout_type',
                    'intensity',
                    'skill_level',
                    'subscription',
                    'required_equipments',
                    'body_focus',
                    'about_video',
                    'additional_info']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about_video': forms.Textarea(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control select-single', 'required': True})
        }
        
    def __init__(self, request, *args, **kwargs):
        super(UpdateVideosForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['subscription'].queryset = VideoSubscription.objects.filter(created_by=request.session.get('user_id'))
        self.fields['language'].widget.choices = user_languages(request.session.get('user_id'))
        
    def save(self, commit=True):
        instance = super(UpdateVideosForm, self).save(commit=False)
        if instance.is_series:
            instance.draft = True
        
        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the video with required_equipments
           instance.required_equipments.clear()
           instance.required_equipments.add(*self.cleaned_data['required_equipments'])
           # This is where we actually link the video with body_focus
           instance.body_focus.clear()
           instance.body_focus.add(*self.cleaned_data['body_focus'])
           # This is where we actually link the video with skill_level
           instance.skill_level.clear()
           instance.skill_level.add(*self.cleaned_data['skill_level'])
        self.save_m2m = save_m2m
        
        if commit:
            instance.save()
            self.save_m2m()
            
        data = self.request.POST.dict()
        file_ids = [ value for key, value in data.items() if key.endswith('_file') and value]
        CommonMedia.objects.filter(id__in=file_ids).update(video = instance)
        return instance

class UpdateSeriesForm(forms.ModelForm):
    subscription = forms.ModelChoiceField(queryset=VideoSubscription.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))

    class Meta:
        model = Videos
        fields = ['name',
                    'language',
                    'subscription',
                    'about_video']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about_video': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'language': forms.Select(attrs={'class': 'form-control select-single', 'required': True})
        }
        
    def __init__(self, request, *args, **kwargs):
        super(UpdateSeriesForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['subscription'].queryset = VideoSubscription.objects.filter(created_by=request.session.get('user_id'))
        self.fields['language'].widget.choices = user_languages(request.session.get('user_id'))
        
    def save(self, commit=True):
        instance = super(UpdateSeriesForm, self).save(commit=False)
        if instance.is_series:
            instance.draft = True
        
        if commit:
            instance.save()
            
        data = self.request.POST.dict()
        file_ids = [ value for key, value in data.items() if key.endswith('_file') and value]
        CommonMedia.objects.filter(id__in=file_ids).update(video = instance)
        return instance
    
class UploadFileForm(forms.ModelForm):
    media_file = forms.FileField()
    class Meta:
        model = CommonMedia
        fields = ['media_file', 'content_name', 'media_type']
    
    def __init__(self, request, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.request = request
        
    def clean(self):
        file = self.cleaned_data.get('media_file', False)
        if not file:
            raise ValidationError('File not found.')
        self.media_type = self.get_mime_type(file)
        
        if self.media_type in settings.IMAGE_TYPES:
            if file.size > settings.IMAGE_UPLOAD_SIZE:
                raise ValidationError(f'Upto {settings.IMAGE_UPLOAD_SIZE} bytes of file size is allowed.')
            
        elif self.media_type in settings.VIDEO_TYPES:
            if file.size > settings.VIDEO_UPLOAD_SIZE:
                raise ValidationError(f'Upto {settings.VIDEO_UPLOAD_SIZE} bytes of file size is allowed.')
        else:
            raise ValidationError('Invalid upload file.')
        return self.cleaned_data
    
    def get_mime_type(self, file):
        """
        Get MIME by reading the header of the file
        """
        initial_pos = file.tell()
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(initial_pos)
        return mime_type
    
    def save(self, commit=True):
        instance = super(UploadFileForm, self).save(commit=False)
        instance.media_type = self.media_type
        if commit:
            instance.save()
        if instance.is_video:
            create_thumbnail(instance)
            instance.duration = get_duration(instance)
            instance.save()
        return instance

class NewEpisodesForm(forms.ModelForm):
    required_equipments = forms.ModelMultipleChoiceField(queryset=EquipmentRequired.objects.all() , required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    body_focus = forms.ModelMultipleChoiceField(queryset=BodyFocus.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    skill_level = forms.ModelMultipleChoiceField(queryset=SkillLevel.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    workout_type = forms.ModelChoiceField(queryset=WorkoutType.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))
    intensity = forms.ModelChoiceField(queryset=Intensity.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))

    class Meta:
        model = SeriesEpisodes
        fields = ['name',
                    'workout_type',
                    'intensity',
                    'skill_level',
                    'required_equipments',
                    'body_focus',
                    'about_video',
                    'additional_info',
                    'series']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'about_video': forms.Textarea(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control'}),
            'series': forms.HiddenInput()
        }
        
    def __init__(self, request, video_id, *args, **kwargs):
        super(NewEpisodesForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['series'].initial = video_id
        
    def save(self, commit=True):
        instance = super(NewEpisodesForm, self).save(commit=False)
         # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the video with required_equipments
           instance.required_equipments.clear()
           instance.required_equipments.add(*self.cleaned_data['required_equipments'])
           # This is where we actually link the video with body_focus
           instance.body_focus.clear()
           instance.body_focus.add(*self.cleaned_data['body_focus'])
           # This is where we actually link the video with skill_level
           instance.skill_level.clear()
           instance.skill_level.add(*self.cleaned_data['skill_level'])
        self.save_m2m = save_m2m
        
        if commit:
            instance.save()
            self.save_m2m()
            
        series = instance.series
        if self.request.POST.get('save_as') == 'draft':
            series.draft = True
        else:
            series.draft = False
            series.visible_to_user = True
        series.save()
        
        data = self.request.POST.dict()
        file_ids = [ value for key, value in data.items() if key.endswith('_file') and value]
        EpisodesMedia.objects.filter(id__in=file_ids).update(series = instance)
        return instance

class EpisodeUpdateForm(forms.ModelForm):
    required_equipments = forms.ModelMultipleChoiceField(queryset=EquipmentRequired.objects.all() , required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    body_focus = forms.ModelMultipleChoiceField(queryset=BodyFocus.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    skill_level = forms.ModelMultipleChoiceField(queryset=SkillLevel.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    workout_type = forms.ModelChoiceField(queryset=WorkoutType.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))
    intensity = forms.ModelChoiceField(queryset=Intensity.objects.all(), empty_label=None, required=True, widget=forms.Select(attrs={'class': 'form-control select-single', 'required': True}))

    class Meta:
        model = SeriesEpisodes
        fields = ['name',
                    'workout_type',
                    'intensity',
                    'skill_level',
                    'required_equipments',
                    'body_focus',
                    'about_video',
                    'additional_info']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'about_video': forms.Textarea(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control'})
        }
        
    def __init__(self, request, *args, **kwargs):
        super(EpisodeUpdateForm, self).__init__(*args, **kwargs)
        self.request = request
    
    def save(self, commit=True):
        instance = super(EpisodeUpdateForm, self).save(commit=False)
         # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the video with required_equipments
           instance.required_equipments.clear()
           instance.required_equipments.add(*self.cleaned_data['required_equipments'])
           # This is where we actually link the video with body_focus
           instance.body_focus.clear()
           instance.body_focus.add(*self.cleaned_data['body_focus'])
           # This is where we actually link the video with skill_level
           instance.skill_level.clear()
           instance.skill_level.add(*self.cleaned_data['skill_level'])
        self.save_m2m = save_m2m
        
        if commit:
            instance.save()
            self.save_m2m()
        
        data = self.request.POST.dict()
        file_ids = [ value for key, value in data.items() if key.endswith('_file') and value]
        EpisodesMedia.objects.filter(id__in=file_ids).update(series = instance)
        return instance
    
# For episodes upload
class EpisodeUploadFileForm(forms.ModelForm):
    media_file = forms.FileField()
    class Meta:
        model = EpisodesMedia
        fields = ['media_file', 'content_name', 'media_type']
    
    def __init__(self, request, *args, **kwargs):
        super(EpisodeUploadFileForm, self).__init__(*args, **kwargs)
        self.request = request
        
    def clean(self):
        file = self.cleaned_data.get('media_file', False)
        if not file:
            raise ValidationError('File not found.')
        self.media_type = self.get_mime_type(file)
        
        if self.media_type in settings.IMAGE_TYPES:
            if file.size > settings.IMAGE_UPLOAD_SIZE:
                raise ValidationError(f'Upto {settings.IMAGE_UPLOAD_SIZE} bytes of file size is allowed.')
            
        elif self.media_type in settings.VIDEO_TYPES:
            if file.size > settings.VIDEO_UPLOAD_SIZE:
                raise ValidationError(f'Upto {settings.VIDEO_UPLOAD_SIZE} bytes of file size is allowed.')
        else:
            raise ValidationError('Invalid upload file.')
        return self.cleaned_data
    
    def get_mime_type(self, file):
        """
        Get MIME by reading the header of the file
        """
        initial_pos = file.tell()
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(initial_pos)
        return mime_type
    
    def save(self, commit=True):
        instance = super(EpisodeUploadFileForm, self).save(commit=False)
        instance.media_type = self.media_type
        if commit:
            instance.save()
        if instance.is_video:
            create_thumbnail(instance)
            instance.duration = get_duration(instance)
            instance.save()
        return instance


# For episodes upload
class ExampleVodForm(forms.ModelForm):
    class Meta:
        model = ExampleVoD
        fields = ['media_file', 'about_video']
        widgets = {
            'media_file': forms.FileInput(attrs={'accept':'video/mp4,video/x-m4v,video/mov,video/avi,video/*'})
        }