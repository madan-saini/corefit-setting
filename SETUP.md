# Use pyffmpeg to generate thumnail of video

Install

`pip install pyffmpeg`
Use

`from pyffmpeg import FFmpeg`

`inf = 'vid.mp4'`
`outf = 'thumb.jpg'`

`ff = FFmpeg()`
`ff.convert(inf, outf)`

Or 
Install django-video-encoding

`pip install django-video-encoding`