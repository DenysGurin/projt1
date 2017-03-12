from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.Welcome.as_view(), name='welcome'),
    url(r'^print/', views.Print.as_view(), name='print'),
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/', views.Logout.as_view(), name='logout'),
    
]