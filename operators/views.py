from django.core.urlresolvers import reverse
from django.views.generic.base import *
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from braces.views import *


class FileImport(LoginRequiredMixin, GroupRequiredMixin, View ):
    group_required = 'operator_paper'

    # help functions
    def is_paper_client(self, user):
        return user.groups.filter(name='paper_client').exists()

    def is_paper_operator(self, user):
        return user.groups.filter(name='paper_operator').exists()

    # end help functions

