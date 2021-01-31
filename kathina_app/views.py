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

scope = ["https://www.googleapis.com/auth/calendar"]
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=scope)
credentials = flow.run_console()

pickle.dump(credentials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))

service = build("calendar", "v3", credentials=credentials)
calendarId = 'primary'

#Define the current day with minimum and maximum limits for event extraction
day_now = datetime.datetime.now().date()
dateMax = str(day_now)+'T23:59:59'
dateMin = str(day_now)+'T00:00:00'

result = service.event().list(calendarId=calendarId, dateMax=dateMax, dateMin=dateMin).execute()


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