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
flow = InstalledAppFlow.from_client_secrets_file(os.path.join(BASE_DIR,"kathina_app/credentials.json"), scopes=scope)

credentials = flow.run_console()

pickle.dump(credentials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))



service = build("calendar", "v3", credentials=credentials)

'''
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])
'''


#Define the current day with minimum and maximum limits for event extraction
day_now = datetime.datetime.now().date()
dateMax = str(day_now)+'T23:59:59.000Z'
dateMin = str(day_now)+'T00:00:00.000Z'

dateMax_obj = datetime.datetime.strptime(dateMax, '%Y-%m-%dT%H:%M:%S.%fZ')
dateMin_obj = datetime.datetime.strptime(dateMin, '%Y-%m-%dT%H:%M:%S.%fZ')

result = service.events().list(calendarId='primary', timeMax = dateMax_obj, timeMin = dateMin_obj, singleEvents = True).execute()




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
            event.start_time = item['start']['dateTime'][11:]
            event.end_time = item['end']['dateTime'][11:]
            event.save()


        return Event.objects.order_by('start_time')




class TaskList(generic.ListView):  # display a list of objects
    template_name = 'kathina_app/index.html'
    context_object_name = 'task_list'

    def get_queryset(self):

        task = Task()
        task.name = 'something'
        task.duration_minutes = 10
        task.save()
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



def add_task(request):
    pass
