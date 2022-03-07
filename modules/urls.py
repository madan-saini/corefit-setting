from django.urls import path, include

urlpatterns = [
    path('vod/', include('modules.video_on_demands.urls')),
    path('classes/', include('modules.classes.urls')),
]
