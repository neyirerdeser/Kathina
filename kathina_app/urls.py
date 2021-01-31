from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EventList.as_view(), name='events'),
]