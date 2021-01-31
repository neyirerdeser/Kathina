from django.shortcuts import render
from django.views import generic

from .models import Event, Task
import datetime
from datetime import timedelta

import pytz
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

service_account_email = "INSERT_HERE"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    filename="FILENAME.json", scopes=SCOPES
)


def build_service():
    service = build("calendar", "v3", credentials=credentials)
    return service


def create_event():
    service = build_service()

    start_datetime = datetime.datetime.now(tz=pytz.utc)
    event = (
        service.events()
        .insert(
            calendarId="CALENDARID@group.calendar.google.com",
            body={
                "summary": "Foo",
                "description": "Bar",
                "start": {"dateTime": start_datetime.isoformat()},
                "end": {
                    "dateTime": (start_datetime + timedelta(minutes=15)).isoformat()
                },
            },
        )
        .execute()
    )


class EventList(generic.ListView):  # display a list of objects
    template_name = 'kathina_app/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.order_by('start_time')


class TaskList(generic.ListView):  # display a list of objects
    template_name = 'kathina_app/index.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        # ...
        # Event.objects
        # Task.objects
        return Event.objects.order_by('start_time')