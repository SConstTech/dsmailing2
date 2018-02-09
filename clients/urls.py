"""dsmailing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
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
from django.views.generic.base import TemplateView
from clients import views as client_views

urlpatterns = [
    url(r'new-document-request/$', client_views.newDocumentRequest.as_view(), name='new-document-request'),
    url(r'add-document-to-request/$', client_views.addDocumentToRequest.as_view(), name='add-document-to-request'),
    url(r'request-processing-status/$', client_views.requestProcessingStatus.as_view(), name='request-processing-status'),
    url(r'request-edit/$', client_views.requestEdit.as_view(), name='request-edit'),
    url(r'request-cancel/$', client_views.requestCancel.as_view(), name='request-cancel'),
    url(r'$', TemplateView.as_view(template_name='home_client.html'), name='home'),
]

#