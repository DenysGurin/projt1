from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Welcome.as_view(), name='welcome'),
    url(r'^print/', views.Print.as_view(), name='print'),
    
]