from django.conf import settings
from flask import request
from .libraries import *
from dateutil.parser import parse


class AddClassTemplate(SuccessMessageMixin, CreateView):
    template_name = 'classes/create-class-template.html'
    model = ClassTemplate
    form_class = NewClassTemplateForm
    pageTitle = 'Create'
    success_url = reverse_lazy('create-class-template')
    success_message = "`%(name)s` has created successfully"

    def get_page_title(self, context):
        return getattr(self, "page_title", settings.SITE_TITLE+" | Create Class Template")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pageTitle"] = self.get_page_title(context)

        return context
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        print(kwargs)
        return kwargs

#@method_decorator(login_required, name='dispatch')
class ClassTemplateListView(SortableListView):
    allowed_sort_fields = {'name': {'default_direction': '-',
                                              'verbose_name': 'Name'},
                           'price': {'default_direction': '',
                                     'verbose_name': 'Price'},
                           'duration': {'default_direction': '',
                                     'verbose_name': 'Duration'},
                           'created_at': {'default_direction': '-',
                                     'verbose_name': 'Creation Date'},}
    default_sort_field = 'created_at'
    
    model = ClassTemplate
    paginate_by = 10
    template_name = 'classes/class-templates.html'
    
    def __init__(self, *args, **kwargs):
        """
        Convert allowed_sort_fields to an OrderedDict data structure to preserve
        ordering if an ordered data structure (e.g. a tuple of tuples) is provided
        """
        super(ClassTemplateListView, self).__init__(*args, **kwargs)
        
    def get_queryset(self):
        queryset = super().get_queryset().filter(user_id=self.request.session.get('user_id'))
        if self.request.GET.get('search'):
            query = self.request.GET.get('search')
            queryset = queryset.filter(Q(name__icontains=query) | Q(about_class__icontains=query)).distinct()
        try:
            start_date = parse(self.request.GET.get('startDate', None)).date()
            end_date = parse(self.request.GET.get('endDate', None)).date()
            queryset = queryset.filter(created_at__lte=end_date, created_at__gte=start_date)
        except Exception as ex:
            print(ex)
        return queryset
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UpdateClassTemplateView(SuccessMessageMixin, UpdateView):
    template_name = 'classes/update_class_template.html'
    model = ClassTemplate
    form_class = UpdateClassTemplateForm
    success_url = reverse_lazy('video_manage_list') 
    success_message = "`%(name)s` has updated successfully"
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class DeleteClassTemplateView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            ClassTemplate.objects.filter(id=id).delete()
            return Response({'success': True})
        except Exception as ex:
            return Response({ 'success': False, 'errors': str(ex)})
            