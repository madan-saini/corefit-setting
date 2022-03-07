from .libraries import *

#@method_decorator(login_required, name='dispatch')
class AddVideoSubscriptionView(SuccessMessageMixin, CreateView):
    template_name = "subscriptions/add.html"
    model = VideoSubscription
    form_class = VideoSubscriptionForm
    success_url = reverse_lazy('video_subscription_list')
    success_message = "Video subscription `%(name)s` has created successfully"
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

#@method_decorator(login_required, name='dispatch')
class UpdateVideoSubscriptionView(SuccessMessageMixin, UpdateView):
    template_name = "subscriptions/update.html"
    model = VideoSubscription
    form_class = VideoSubscriptionUpdateForm
    success_url = reverse_lazy('video_subscription_list')
    success_message = "Video subscription `%(name)s` has updated successfully"
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

#@method_decorator(login_required, name='dispatch')
class VideoSubscriptionsView(SortableListView):
    model = VideoSubscription
    paginate_by = 10
    template_name = 'subscriptions/index.html'
    
    allowed_sort_fields = {'name': {'default_direction': '',
                                     'verbose_name': 'Name'},
                           'price': {'default_direction': '',
                                     'verbose_name': 'Price'},
                           'created_at': {'default_direction': '-',
                                     'verbose_name': 'Created At'},}
    default_sort_field = 'created_at'
    
    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.session.get('user_id'))

class DeleteVideoSubscriptionView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            objects = VideoSubscription.objects.filter(id=id)
            if objects.last().can_delete:
                objects.delete()
                return Response({'success': True})
            return Response({'success': False, 'errors': 'This subscription is being used by other resource.'})
        except Exception as ex:
            return Response({ 'success': False, 'errors': str(ex)})

class CheckVideoSubscriptionView(APIView):
    """ CHeck if any new video ca be added on this subscription id or not by total_video column value"""
    def get(self, request, id, *args, **kwargs):
        try:
            obj = VideoSubscription.objects.get(id=id)
            if obj.videos.count() < obj.total_videos:
                return Response({'success': True})
            return Response({'success': False, 'errors': f"Subscription's total videos limit {obj.total_videos} already has reached."})
        except Exception as ex:
            return Response({ 'success': False, 'errors': str(ex)})