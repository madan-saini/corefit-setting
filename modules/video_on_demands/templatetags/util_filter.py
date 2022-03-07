from django import template
register = template.Library()
from modules.video_on_demands.models import CommonMedia

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def profile_image(video):
    common_media = video.commonmedia_set.filter(content_name='Profile Image', media_type__contains='image').last()
    return common_media

@register.simple_tag
def tile_image(video):
    common_media = video.commonmedia_set.filter(content_name='Tile Image', media_type__contains='image').last()
    return common_media

@register.simple_tag
def uploaded_video(video):
    common_media = video.commonmedia_set.filter(content_name='Video', media_type__contains='video').last()
    return common_media

@register.simple_tag
def uploaded_teaser(video):
    common_media = video.commonmedia_set.filter(content_name='Video Teaser', media_type__contains='video').last()
    return common_media

# Episodes
@register.simple_tag
def episode_profile_image(video):
    common_media = video.episodesmedia_set.filter(content_name='Profile Image', media_type__contains='image').last()
    return common_media

@register.simple_tag
def episode_tile_image(video):
    common_media = video.episodesmedia_set.filter(content_name='Tile Image', media_type__contains='image').last()
    return common_media

@register.simple_tag
def episode_uploaded_video(video):
    common_media = video.episodesmedia_set.filter(content_name='Video', media_type__contains='video').last()
    return common_media

@register.simple_tag
def episode_uploaded_teaser(video):
    common_media = video.episodesmedia_set.filter(content_name='Video Teaser', media_type__contains='video').last()
    return common_media