from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView

class IndexPageView(RedirectView):
    permanent = False

    # help functions
    def is_paper_client(self, user):
        return user.groups.filter(name='paper_clients').exists()

    def is_paper_operator(self, user):
        return user.groups.filter(name='paper_operators').exists()

    def is_admin(self, user):
        return user.groups.filter(name='administrator').exists()

    # end help functions

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if self.is_client(self.request.user):
                return reverse('clients:home')
            elif self.is_operator(self.request.user): #and not is_admin(request.user):
                return reverse('operators:home')
            elif self.is_admin(self.request.user):
                return reverse('administrators:home')
            else:
                return reverse('system:home')