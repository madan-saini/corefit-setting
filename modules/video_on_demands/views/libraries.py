import pdb
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from modules.video_on_demands.models import VideoSubscription, Videos, ExampleVoD, SeriesEpisodes
from modules.video_on_demands.forms import VideoSubscriptionUpdateForm, VideoSubscriptionForm, NewVideosForm, NewSeriesForm, UpdateVideosForm, UpdateSeriesForm, NewEpisodesForm, EpisodeUpdateForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from sortable_listview import SortableListView
from django.contrib.messages import success, error, warning, info
from rest_framework.views import APIView
from rest_framework.response import Response