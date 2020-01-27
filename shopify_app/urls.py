from django.urls import path

from . import views

app_name = 'shopify_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('install/', views.Install.as_view(), name='install'),
    path('authenticate/', views.Authenticate.as_view(), name='authenticate'),
    path('finalize/', views.Finalize.as_view(), name='finalize'),
    path('subscribe/', views.Subscribe.as_view(), name='subscribe'),
    path('subscribe/submit', views.SubmitSubscribe.as_view(), name='subscribe_submit'),
    path('webhook/app_uninstalled/', views.WebhookAppUninstalled.as_view(), name='app_uninstalled'),
    path('proxy_url/', views.MainXml.as_view(), name='main_xml'),
    path('proxy_url/google.xml', views.GoogleXml.as_view(), name='google_xml'),
    path('proxy_url/facebook.xml', views.FacebookXml.as_view(), name='facebook_xml'),
    path('proxy_url/yottos.xml', views.YottosXml.as_view(), name='yottos_xml'),
    path('proxy_url/pinterest.xml', views.PinterestXml.as_view(), name='pinterest_xml'),
]
