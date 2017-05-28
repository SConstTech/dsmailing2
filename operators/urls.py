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
from django.contrib import admin
from django.views.generic.base import TemplateView
from operators.views import *


urlpatterns = [
    url(r'add-new-base$', FileImport.as_view(), name='file-upload'),
    url(r'preview$', PreviewView.as_view(), name='preview'),
    url(r'create-client$', ClientCreate.as_view(), name='create-client'),
    url(r'barcode-checker$', BarcodeChecker.as_view(), name='barcode-checker'),
    url(r'export-by-date$', ExportReport.as_view(), name='export-by-date'),
    url(r'create-project$', ProjectCreate.as_view(), name='create-project'),
    url(r'^$', HomeView.as_view(), name='home'),

]
