import pdb, json
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import CommonMedia, Videos
from django.views.generic import View
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from .forms import UploadFileForm, EpisodeUploadFileForm

class UpdateVisibleToUserView(APIView):
    def get(self, request, id, visible,  *args, **kwargs):
        try:
            obj = Videos.objects.get(id=id)
            obj.visible_to_user = True if visible == 'yes' else False
            obj.save()
            return Response("Updated")
        except Exception as ex:
            return Response(ex)

# For Videos & Series only
class UploadNewMediaFileView(View, FormMixin):
    form_class = UploadFileForm
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        try:
            form = self.get_form()
            if form.is_valid():
                instance = form.save()
                return HttpResponse(json.dumps({'id': instance.id, 'name': instance.content_name, 'duration': instance.duration, 'success': True, 'thumb': instance.get_thumbnail}))
            return HttpResponse(json.dumps({'success': False, 'errors': form.errors}))
        except Exception as ex:
            print(ex)
            return HttpResponse(json.dumps({'success': False, 'errors': str(ex)}))
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

# For Episodes only
class UploadEpisodesMediaFileView(View, FormMixin):
    form_class = EpisodeUploadFileForm
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        try:
            form = self.get_form()
            if form.is_valid():
                instance = form.save()
                return HttpResponse(json.dumps({'id': instance.id, 'name': instance.content_name, 'duration': instance.duration, 'success': True, 'thumb': instance.get_thumbnail}))
            return HttpResponse(json.dumps({'success': False, 'errors': form.errors}))
        except Exception as ex:
            print(ex)
            return HttpResponse(json.dumps({'success': False, 'errors': str(ex)}))
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class GetVideoUrl(APIView):
    def get(self, request, video_id,  *args, **kwargs):
        try:
            obj = CommonMedia.objects.get(id=video_id)
            return Response({'code': 200, 'src': obj.media_file.url})
        except Exception as ex:
            return Response({'code': 500, 'src': '' , 'error': str(ex)})