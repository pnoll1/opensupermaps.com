from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.downloads),
    path('contact', views.contact),
    path('faq', views.faq),
    #path('downloads-ad', views.downloads_ad),
    #re_path(r'^downloads/static',views.serve_downloads),
    #path('login', views.login_view),
    #path('logout', views.logout_view),
    #path('change-password/', auth_views.PasswordChangeView.as_view(success_url='/password-change-done/')),
    #path('password-change-done/', auth_views.PasswordChangeDoneView.as_view()),
    #path('register', views.register),
    #path('payment', views.payment),
    #path('webhooks', views.webhook_view),
    # path('tax', views.tax),
]
