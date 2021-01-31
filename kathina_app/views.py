from django.shortcuts import render
from django.views import generic

from .models import Event, Task

class EventList(generic.ListView):  # display a list of objects
    template_name = 'kathina_app/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.order_by('start_time')
