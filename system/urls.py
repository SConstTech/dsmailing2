"""dsmailing URL Configuration
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from system.views import *


urlpatterns = [
    url(r'login$', auth_views.login, {'template_name':'system/login.html'}, name='login'),
    url(r'logout$', auth_views.logout,  {'next_page': '/'}, name='logout'),
    url(r'home$', TemplateView.as_view(template_name='system/base_site.html'), name='home'),
    url(r'$', IndexPageView.as_view(), name='index'),
]
