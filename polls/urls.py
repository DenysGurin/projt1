from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Polls.as_view(), name='polls'),
    url(r'^test/(?P<poll_id>[0-9]+)/$', views.Test.as_view(), name='test'),
    #url(r'^test(?P<question_id>[0-9]+)/$', views.Test.as_view(), name='test'),
]