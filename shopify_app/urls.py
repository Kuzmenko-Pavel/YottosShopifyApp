from django.urls import path
from . import views

app_name = 'shopify_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('install/', views.install, name='install'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('finalize/', views.finalize, name='finalize'),
    path('webhook/app_uninstalled/', views.webhook_app_uninstalled, name='app_uninstalled'),
]
