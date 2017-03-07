from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Welcome.as_view(), name='welcome'),
    url(r'^singin/$', views.Singin.as_view(), name='singin'),
    url(r'^login/$', views.Login.as_view(), name='login'),
]