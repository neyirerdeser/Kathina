from django.shortcuts import render
from django.views import generic

from .models import Event, Task
import datetime
import pickle
import os.path
from datetime import date

import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


scope = ["https://www.googleapis.com/auth/calendar"]
flow = InstalledAppFlow.from_client_secrets_file(os.path.join(BASE_DIR,"kathina_app/credentials.json"), scopes=scope)

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
    template_name = 'kathina_app/events.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        Event.objects.all().delete()
        # create new event objects from result
        items = result['items']
        for item in items:
            event = Event()
            event.name = item['summary']

            start_time = item['start']['dateTime'][11:]
            hst = int(start_time[:2])
            hstd = int(start_time[9:11])
            mst = int(start_time[3:5])
            mstd = int(start_time[12:14])
            start = datetime.datetime.now().replace(hour = hst + hstd, minute = mst + mstd, second = 0).time()
            end_time = item['end']['dateTime'][11:]
            het = int(end_time[:2])
            met = int(start_time[3:5])
            hetd = int(end_time[9:11])
            metd = int(end_time[12:14])
            end = datetime.datetime.now().replace(hour = het + hetd, minute = met + metd, second = 0).time()

            event.start_time = start
            event.end_time = end
            event.save()


        return Event.objects.order_by('start_time')




class TaskList(generic.ListView):  # display a list of objects
    template_name = 'kathina_app/tasks.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        #
        # task = Task()
        # task.name = 'something'
        # task.duration_minutes = 10
        # task.save()
        return Task.objects.order_by('duration_minutes')


def smart_scheduler():
    taskList = Task.objects.all()
    eventList = Event.objects.all()
    smartList = eventList

    pref_start_time = datetime.datetime.now().replace(hour=9)
    pref_end_time = datetime.datetime.now().replace(hour=23)

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

class DayView(generic.ListView):
    template_name = 'kathina_app/day.html'
    context_object_name = 'day_list'

    def get_queryset(self):
        return smart_scheduler()

def add_task(request):
    pass
