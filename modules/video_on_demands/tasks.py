from django.core.files import File
from video_encoding.backends import get_backend
import os, re
from .models import CommonMedia
import subprocess 

def create_thumbnail(video):
   if not video.media_file:
      # no video file attached
      return

   if video.has_thumb:
      # thumbnail has already been generated
      return

   encoding_backend = get_backend()
   thumbnail_path = encoding_backend.get_thumbnail(video.media_file.path)
   filename = os.path.basename(video.media_file.path+".png"),

   try:
      with open(thumbnail_path, 'rb') as file_handler:
         django_file = File(file_handler)
         video.thumbnail.save(filename, django_file)
      video.save()
   finally:
      os.unlink(thumbnail_path)

def get_video_info(video):
   # Return duration, width and height of the video.
   if not video.media_file:
      # no video file attached
      return
   encoding_backend = get_backend()
   video_info = encoding_backend.get_media_info(video.media_file.path)
   return video_info


# Other way
def get_duration(video):
   """Get the duration of a video using ffprobe."""
   if not video.media_file:
      # no video file attached
      return
   cmd = 'ffprobe -i {} -v quiet -show_entries format=duration -hide_banner -of default=noprint_wrappers=1:nokey=1 -sexagesimal'.format(video.media_file.path)
   output = subprocess.check_output(
      cmd,
      shell=True, # Let this run in the shell
      stderr=subprocess.STDOUT
   )
   duration = re.sub('\.+.*|\n', '', output.decode())
   return duration