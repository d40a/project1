from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^get_data/', views.get_data),
	url(r'^details_of_test/', views.details_of_test),
]
