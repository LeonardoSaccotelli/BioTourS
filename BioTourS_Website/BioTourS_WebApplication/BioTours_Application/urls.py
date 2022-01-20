# File urls which manage the urls of rolls app
from django.urls import path
from . import views

# URLS.PY FILE OF BioTourS_Application Component

urlpatterns = [
    path('', views.HomepageView, name="index"),
    path('about/', views.AboutView, name="about"),
    path('insert/', views.InsertSightingView, name="insertSighting"),
    path('showSighting/', views.ShowSightingView, name='showSighting'),
    # path('<int:pk>/sightingDetails', views.DetailSightingView.as_view(), name='sightingDetails'),
    path('mapViewer/', views.MapViewerView, name='mapViewer'),
    path('gallery/', views.GalleryView, name='gallery'),
    path('sightingDetails/<int:sighting_pk>', views.DetailSightingView, name='sightingDetails'),
]
