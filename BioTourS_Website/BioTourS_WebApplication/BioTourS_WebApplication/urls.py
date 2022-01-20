"""BioTourS_WebApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    ------------------------------------------------------------------
    GENERAL URLS.PY FILE
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('biotours/admin/', admin.site.urls),

    # Including the BioTourS_Application urls.py file, while handles
    # the urls' application. The 'biotours/' url defines the homepage's
    # url.
    # The file urls.py of BioToursApplication handles the sub-urls of
    # 'biotours/'
    path('biotours/', include('BioTours_Application.urls')),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
