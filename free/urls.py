from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.downloads),
    path('contact', views.contact),
    path('faq', views.faq),
]
