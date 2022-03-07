from flask import request
from .libraries import *
from dateutil.parser import parse
from django.db.models import Q
#@method_decorator(login_required, name='dispatch')
class VideoIndex(TemplateView):
    template_name = 'videos/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['examples'] = ExampleVoD.objects.all()
        return context

#@method_decorator(login_required, name='dispatch')
class VideosListView(SortableListView):
    allowed_sort_fields = {
        'name': {'default_direction': '',
                 'verbose_name': 'Name'},
        'is_series': {'default_direction': '-',
                      'verbose_name': 'Type'},
        'subscription': {'default_direction': '-',
                      'verbose_name': 'Subscription'},
        'created_at': {'default_direction': '-',
                       'verbose_name': 'Creation Date'},}
    default_sort_field = 'created_at'
    
    model = Videos
    paginate_by = 10
    template_name = 'videos/list_videos.html'
    
    def __init__(self, *args, **kwargs):
        """
        Convert allowed_sort_fields to an OrderedDict data structure to preserve
        ordering if an ordered data structure (e.g. a tuple of tuples) is provided
        """
        super(VideosListView, self).__init__(*args, **kwargs)
        
    def get_queryset(self):
        queryset = super().get_queryset().filter(created_by=self.request.session.get('user_id'))
        query = Q()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            query |= Q(name__icontains=search) 
            query |= Q(about_video__icontains=search)
        try:
            if self.request.GET.get('startDate', None):
                start_date = parse(self.request.GET.get('startDate', None)).date()
                query &= Q(created_at__gte=start_date)
            
            if self.request.GET.get('endDate', None):
                end_date = parse(self.request.GET.get('endDate', None)).date()
                query &= Q(created_at__lte=end_date)
        except Exception as ex:
            print(ex)
        
        try:
            if self.request.GET.get('vtype', None):
                vidType = self.request.GET.get('vtype')
                if vidType == 'series':
                    query &= Q(is_series=True)
                else:
                    query &= Q(is_series=False)
            
            if self.request.GET.get('subscription', None):
                query &= Q(subscription_id=self.request.GET.get('subscription'))
        except Exception as ex:
            print(ex)
        
        return queryset.filter(query).distinct()
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriptions'] = VideoSubscription.objects.filter(created_by=self.request.session.get('user_id'))
        return context
#@method_decorator(login_required, name='dispatch')
class AddVideoView(SuccessMessageMixin, CreateView):
    template_name = 'videos/create.html'
    model = Videos
    form_class = NewVideosForm
    success_url = reverse_lazy('video_manage_list')
    success_message = "`%(name)s` has created successfully"
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        if self.object and self.object.is_series:
            # Redirect to add new episodes
            return HttpResponseRedirect(reverse_lazy('series_episodes_add', kwargs={'id': self.object.id }))
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab'] = 'video'
        return context

#@method_decorator(login_required, name='dispatch')
class UpdateVideoView(SuccessMessageMixin, UpdateView):
    template_name = 'videos/update.html'
    model = Videos
    form_class = UpdateVideosForm
    success_url = reverse_lazy('video_manage_list')
    success_message = "`%(name)s` has updated successfully"
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class DeleteVideoView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            Videos.objects.filter(id=id).delete()
            return Response({'success': True})
        except Exception as ex:
            return Response({ 'success': False, 'errors': str(ex)})