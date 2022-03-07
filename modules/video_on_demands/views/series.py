from .libraries import *

#@method_decorator(login_required, name='dispatch')
class AddSeriesView(SuccessMessageMixin, CreateView):
    template_name = 'series/create.html'
    model = Videos
    form_class = NewSeriesForm
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
        context['tab'] = 'series'
        return context

#@method_decorator(login_required, name='dispatch')
class UpdateSeriesView(SuccessMessageMixin, UpdateView):
    template_name = 'series/update.html'
    model = Videos
    form_class = UpdateSeriesForm
    success_url = reverse_lazy('video_manage_list')
    success_message = "`%(name)s` has updated successfully"
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['episodes'] = self.object.seriesepisodes_set.all()
        return context