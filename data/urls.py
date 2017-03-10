from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Data.as_view(), name='data'),
    
]