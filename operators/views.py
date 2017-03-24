from django.core.urlresolvers import reverse
from django.views.generic.base import *
from django.shortcuts import *
from django.http import *
from braces.views import *


class FileImport(GroupRequiredMixin, View ):
    group_required = u'paper_operator'
    # http_method_names = ['GET', 'POST']

    def get(self, request):
        return render(request, template_name='import/import-file.jinja' )
    def post(self,request):
        pass




class HomeView(GroupRequiredMixin, TemplateView):
    group_required = 'paper_operator'
    template_name='index_operator.jinja'