from django.urls import path
from .views.classes import AddClassTemplate, ClassTemplateListView, UpdateClassTemplateView, DeleteClassTemplateView

urlpatterns = [
    path('create-class-template', AddClassTemplate.as_view(), name='create-class-template'),
    path('class-templates', ClassTemplateListView.as_view(), name='class-templates'),
    path('class/<pk>/update', UpdateClassTemplateView.as_view(), name='class_update'),
    path('class/<id>/delete', DeleteClassTemplateView.as_view(), name='class_delete'),
    # path('upload', UploadClassMediaView.as_view(), name='upload-class-media'),
    # path('<id>/template/add', AddTemplateView.as_view(), name='template_add'),
    # path('add', AddClassView.as_view(), name='create_class_template'),
]
