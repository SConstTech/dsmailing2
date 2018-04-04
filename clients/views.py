
from django.views.generic.base import *
from django.views.generic.list import *
from django.shortcuts import *
from django.http import *
from braces.views import *
from system.models import *
import xlrd, datetime, csv
from datetime import timedelta
from django.http import HttpResponse
import time


# class newDocumentRequest(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
#     group_required = 'client'
#     template_name='client/document-request/new-request.html'
#
# class addDocumentToRequest(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
#     group_required = 'client'
#     template_name='client/home_client.html'
#
# class requestProcessingStatus(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
#     group_required = 'client'
#     template_name = 'client/home_client.html'
#
# class requestEdit(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
#     group_required = 'client'
#     template_name = 'client/home_client.html'
#
# class requestCancel(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
#     group_required = 'client'
#     template_name = 'client/home_client.html'

class NewRequest(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = 'client'
    http_method_names = ['GET']
    template_name = 'client/new-request.html'

class CancelRequest(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = 'client'
    template_name = 'client/home_client.html'

class TrackProgress(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = 'client'
    template_name = 'client/home_client.html'

class itemAdd(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = 'client'
    template_name = 'client/home_client.html'


class itemRemove(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    group_required = 'client'
    template_name = 'client/home_client.html'
