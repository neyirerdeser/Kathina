from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EventList.as_view(), name='events'),
    url(r'^$', views.TaskList.as_view(), name='tasks'),
    url(r'^$', views.DayView.as_view(), name='day'),
]