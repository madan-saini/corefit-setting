from django.urls import path
from .views.series import AddSeriesView, UpdateSeriesView
from .views.videos import VideoIndex, AddVideoView, UpdateVideoView, DeleteVideoView, VideosListView
from .views.subscriptions import CheckVideoSubscriptionView, AddVideoSubscriptionView, VideoSubscriptionsView, UpdateVideoSubscriptionView, DeleteVideoSubscriptionView
from .views.episodes import AddEpisodesView, UpdateEpisodesView, DeleteEpisodeView
from .apis import UpdateVisibleToUserView, UploadNewMediaFileView, UploadEpisodesMediaFileView, GetVideoUrl

urlpatterns = [
    path('', VideoIndex.as_view(), name='video_on_demand_index'),
    path('subscription/add', AddVideoSubscriptionView.as_view(), name='video_subscription_add'),
    path('subscriptions', VideoSubscriptionsView.as_view(), name='video_subscription_list'),
    path('subscription/<pk>/update', UpdateVideoSubscriptionView.as_view(), name='video_subscription_update'),
    path('subscription/<id>/delete', DeleteVideoSubscriptionView.as_view(), name='video_subscription_delete'),
    path('check-limit/<id>/subs', CheckVideoSubscriptionView.as_view(), name='video_subscription_limit'),
    path('add', AddVideoView.as_view(), name='video_series_add'),
    path('series', AddSeriesView.as_view(), name='new_series_add'),
    path('video/<pk>/update', UpdateVideoView.as_view(), name='video_update'),
    path('video/<id>/delete', DeleteVideoView.as_view(), name='video_delete'),
    path('series/<pk>/update', UpdateSeriesView.as_view(), name='video_series_update'),
    path('manages', VideosListView.as_view(), name='video_manage_list'),
    path('<id>/update/<visible>', UpdateVisibleToUserView.as_view(), name='video_visibility_update'),
    path('upload', UploadNewMediaFileView.as_view(), name='upload-new-video'),
    path('upload/episode', UploadEpisodesMediaFileView.as_view(), name='upload-episode-media'),
    path('<id>/episode/add', AddEpisodesView.as_view(), name='series_episodes_add'),
    path('episode/<pk>/update', UpdateEpisodesView.as_view(), name='series_episode_update'),
    path('episode/<pk>/delete', DeleteEpisodeView.as_view(), name='series_episode_delete'),
    path('link/<video_id>', GetVideoUrl.as_view(), name='get_video_link')
]
