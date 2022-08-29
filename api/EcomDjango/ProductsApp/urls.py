from django.urls import include, re_path
from ProductsApp import views

from django.conf.urls.static import static
from django.conf import settings
# All the url declarations needed for this project


#specifying the roots for our api methods
urlpatterns=[
    re_path(r'^product$', views.productApi),
    re_path(r'^product/([0-9]+)$', views.productApi),

    re_path(r'^product/savefile', views.SaveFile)
    
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
