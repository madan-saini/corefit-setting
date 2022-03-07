from .libraries import *

#@method_decorator(login_required, name='dispatch')
class AddEpisodesView(SuccessMessageMixin, CreateView):
    template_name = 'episodes/create.html'
    model = SeriesEpisodes
    form_class = NewEpisodesForm
    success_url = reverse_lazy('video_manage_list')
    success_message = "`%(name)s` has created successfully"
    
    def get(self, request, *args, **kwargs):
        self.object = None
        result = super().get(request, *args, **kwargs)
        context = self.get_context_data()
        if context.get('video').is_series:
            return result
        error(request, "Only series can have episodes.")
        return HttpResponseRedirect(reverse_lazy('video_manage_list'))
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request, 'video_id': self.kwargs.get('id')})
        return kwargs
    
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        if self.request.POST.get('save_as') == 'draft':
            # Redirect to add new episodes
            return HttpResponseRedirect(reverse_lazy('series_episodes_add', kwargs={'id': self.object.series.id }))
        return result
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        video = Videos.objects.get(id=self.kwargs.get('id'))
        context['video'] = video
        context['next_episodes'] = video.seriesepisodes_set.count() +1
        return context

#@method_decorator(login_required, name='dispatch')
class UpdateEpisodesView(SuccessMessageMixin, UpdateView):
    template_name = 'episodes/update.html'
    model = SeriesEpisodes
    form_class = EpisodeUpdateForm
    success_url = reverse_lazy('video_manage_list')
    success_message = "`%(name)s` has updated successfully"
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
class DeleteEpisodeView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            SeriesEpisodes.objects.filter(id=pk).delete()
            return Response({'success': True})
        except Exception as ex:
            return Response({ 'success': False, 'errors': str(ex)})