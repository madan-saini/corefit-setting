# importing the module
from pytube import YouTube
from pytube.cli import on_progress
import os, sys
# where to save
SAVE_PATH = os.path.join(os.getcwd(), 'videos') #to_do

# link of the video to be downloaded
link = sys.argv[1]

fuchsia = '\033[38;2;255;00;255m'   #  color as hex #FF00FF
reset_color = '\033[39m'
            
# object creation using YouTube
# which was imported in the beginning
yt = YouTube(link, on_progress_callback=on_progress)
print(f'\n' + fuchsia + 'Downloading: ', yt.title, '~ viewed', yt.views, 'times.')
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(SAVE_PATH)
print(f'\nFinished downloading:  {yt.title}' + reset_color)

