import pdb
from typing_extensions import Required
# from tkinter import Widget
from django import forms
from gymstudio.models import Language, User, Currency
from .models import WorkoutType, CommonMedia, Intensity, ClassTemplate, BodyFocus, EquipmentRequired,  SkillLevel
from djmoney.forms import MoneyField
from django.core.exceptions import ValidationError
import magic
from django.conf import settings
from .tasks import create_thumbnail, get_duration

def user_languages(user_id):
    try:
        user_langs = User.objects.get(id=user_id).languages.split(',')
        return tuple(Language.objects.filter(id__in=user_langs).values_list('id', 'name'))
    except:
        return ()
 
class NewClassTemplateForm(forms.ModelForm):
    
    class_template = forms.ModelChoiceField(queryset=ClassTemplate.objects.all(), empty_label="Create New Template", required=False, widget=forms.Select(attrs={'class': 'multiple-single','onchange':'getTemplateData(this.value)'}))
    required_equipments = forms.ModelMultipleChoiceField(queryset=EquipmentRequired.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    body_focus = forms.ModelMultipleChoiceField(queryset=BodyFocus.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    skill_level = forms.ModelMultipleChoiceField(queryset=SkillLevel.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes', 'required': True}))
    # language = forms.ModelChoiceField(queryset=Language.objects.all(), empty_label="Select Language", required=False, widget=forms.Select(attrs={'class': 'multiple-single'}))
    intensity = forms.ModelChoiceField(queryset=Intensity.objects.all(), empty_label="Select Intensity", required=False, widget=forms.Select(attrs={'class': 'multiple-single required', 'required': True}))
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), blank=False, required=False, widget=forms.Select(attrs={'class': 'single-withoutsearch required','defualt':'USD'}))

    class Meta:
        model = ClassTemplate
        fields = ['name',
                    'language',
                    'intensity',
                    'subscriber_limit',
                    'skill_level',
                    'duration',
                    'required_equipments',
                    'body_focus',
                    'currency',
                    'price',
                    'about_class',
                    'additional_info',
                    'user_id',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'subscriber_limit': forms.TextInput(attrs={'class': 'digits','min': '0'}),
            'price': forms.TextInput(attrs={'class': 'required digits','min':'0'}),
            'duration': forms.TextInput(attrs={'min': '1','max': '1440','class': 'required'}),
            'about_class': forms.Textarea(attrs={'class': 'form-control required','style':'resize: none;'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control','style':'resize: none;'}),
            'language': forms.Select(attrs={'class': 'multiple-single', 'required': True}),
            # 'intensity': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'user_id': forms.HiddenInput()
        }
    
    def __init__(self, request, *args, **kwargs):
        
        super(NewClassTemplateForm, self).__init__(*args, **kwargs)
        self.request = request
        user = request.session.get('user_id', 0)
        self.fields['user_id'].initial = user
        self.fields['language'].widget.choices = user_languages(request.session.get('user_id'))

    def save(self, commit=True): 
        instance = super(NewClassTemplateForm, self).save(commit=False)
        instance.skill_level = self.cleaned_data.get('skill_level')
        # instance.required_equipments.clear()
        # instance.required_equipments.add(*self.cleaned_data['required_equipments'])
        # instance.skill_level.set(*self.cleaned_data['skill_level'])
        # if instance.is_series:
        #     instance.draft = True
        
        # print('ttttyy--',self)
        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        
        def save_m2m():
            
            old_save_m2m()
            # print(old_save_m2m)
            # print('run')
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

class UpdateClassTemplateForm(forms.ModelForm):
    # class_template = forms.ModelChoiceField(queryset=ClassTemplate.objects.all(), empty_label="Create New Template", required=False, widget=forms.Select(attrs={'class': 'multiple-single','onchange':'getTemplateData(this.value)'}))
    required_equipments = forms.ModelMultipleChoiceField(queryset=EquipmentRequired.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes'}))
    body_focus = forms.ModelMultipleChoiceField(queryset=BodyFocus.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes'}))
    skill_level = forms.ModelMultipleChoiceField(queryset=SkillLevel.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'multiple-checkboxes'}))
    language = forms.ModelChoiceField(queryset=Language.objects.all(), empty_label="Select Language", required=False, widget=forms.Select(attrs={'class': 'multiple-single'}))
    intensity = forms.ModelChoiceField(queryset=Intensity.objects.all(), empty_label="Select Intensity", required=False, widget=forms.Select(attrs={'class': 'single-withoutsearch'}))
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), blank=False, required=False, widget=forms.Select(attrs={'class': 'single-withoutsearch required','defualt':'USD'}))

    class Meta:
        model = ClassTemplate
        fields = ['name',
                    'language',
                    'intensity',
                    'subscriber_limit',
                    'skill_level',
                    'duration',
                    'required_equipments',
                    'body_focus',
                    'currency',
                    'price',
                    'about_class',
                    'additional_info']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'subscriber_limit': forms.TextInput(attrs={'class': ''}),
            'price': forms.TextInput(attrs={'class': 'required'}),
            'duration': forms.TextInput(attrs={'min': '1','max': '1440','class': 'required'}),
            'about_class': forms.Textarea(attrs={'class': 'form-control required','style':'resize: none;'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control required','style':'resize: none;'}),
        }
        
    def __init__(self, request, *args, **kwargs): 
        super(UpdateClassTemplateForm, self).__init__(*args, **kwargs)
        self.request = request
        # self.fields['subscription'].queryset = VideoSubscription.objects.filter(created_by=request.session.get('user_id'))
        
    def save(self, commit=True):
        instance = super(UpdateClassTemplateForm, self).save(commit=False)
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