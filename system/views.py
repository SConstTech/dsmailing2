from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404

class IndexPageView(RedirectView):
    permanent = False

    # help functions
    def is_paper_client(self, user):
        return user.groups.filter(name='paper_client').exists()

    def is_paper_operator(self, user):
        return user.groups.filter(name='paper_operator').exists()

    # end help functions

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if self.is_paper_client(self.request.user):
                return reverse('clients:home')
            elif self.is_paper_operator(self.request.user): #and not is_admin(request.user):
                return reverse('operators:home')
            else:
                raise Http404


def custom_login(request):
    #{'template_name': 'login.html', 'redirect_field_name': 'system'}
    if request.user.is_authenticated():
        return HttpResponseRedirect('system:index')
    else:
        return auth_views.login(request, template_name='login.html')

def custom_logout(request):
    logout(request)
    return redirect('/')
