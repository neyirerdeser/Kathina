from django.shortcuts import render
from django.views import generic

from .models import Event, Task
import datetime
import pickle
import os.path
from datetime import timedelta

import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

scope = ["https://www.googleapis.com/auth/calendar"]
flow = InstalledAppFlow.from_client_secrets_file(os.path.join(BASE_DIR,"kathina_app\credentials.json"), scopes=scope)
credentials = flow.run_console()

pickle.dump(credentials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))


def build_service():
    service = build("calendar", "v3", credentials=credentials)
    return service


def create_event():
    service = build_service()
    start_datetime = datetime.datetime.now(tz=pytz.utc)
    event = (
        service.events()
        .insert(
            calendarId="primary",
            body={
                "summary": "This is an event yay!",
                "description": "It worked!",
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

    def smart_scheduler(self):
        taskList = Task.objects.all()
        eventList = Event.objects.all()
        smartList = eventList

        pref_start_time = DateTime.Today.AddHours(9)
        pref_end_time = DateTime.Today.AddHours(23)

        #TODO: Need to code for overflowing end times (by going into the next day)

        start_counter = pref_start_time
        for i in range(len(taskList)):
            taskTime = taskList[i].duration_with_breaks

            for j in range(len(smartList)):
                if taskTime <= smartList[j].start_time - start_counter:
                    taskAsEvent = Event()
                    taskAsEvent.name = taskList[i].name
                    taskAsEvent.start_time = start_counter
                    taskAsEvent.end_time = start_counter + taskTime

                    smartList.insert(taskAsEvent, j)
                    start_counter = start_counter + taskTime
                    break
                else:
                    start_counter = smartList[j].end_time

        return smartList

create_event()