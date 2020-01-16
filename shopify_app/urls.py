from django.urls import path
from . import views

app_name = 'shopify_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('install/', views.install, name='install'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('finalize/', views.finalize, name='finalize'),
    path('webhook/app_uninstalled/', views.webhook_app_uninstalled, name='app_uninstalled'),
    path('proxy_url/google.xml', views.google_xml, name='google_xml'),
    path('proxy_url/facebook.xml', views.facebook_xml, name='facebook_xml'),
    path('proxy_url/yottos.xml', views.yottos_xml, name='yottos_xml'),
]
