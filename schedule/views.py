from django.shortcuts import render

import os
import random
from collections import Counter
import requests
import json
from datetime import datetime


APP_ACTIVITIES = [
    "Lunch",
    "Coding",
    "Documentation/Blog Writing",
    "Meetings",
    "Help a team member",
    "Code review",
    "Watch a demo",
]

APP_FEELINGS = {
    "annoyed": {"work": [5, 0, 0, 0, 10, 10, 10]},
    "bored": {"work": [5, 10, 0, 0, 5, 0, 5]},
    "cool": {"work": [0, 10, 10, 10, 10, 0, 0]},
    "hot": {"work": [5, 5, 5, 5, 0, 2, 5]},
    "nervous": {"work": [10, 5, 2, 0, 0, 0, 5]},
    "quiet": {"work": [5, 10, 0, 0, 0, 0, 10]},
    "sick": {"work": [0, 0, 0, 0, 0, 0, 0], "pto": 5},
    "sleep": {"work": [5, 1, 0, 0, 5, 0, 0]},
}

APP_WORKING_HOURS = 8

APP_PLANNINGS_BASE_URL = "http://127.0.0.1:8000/plannings/"

def home(request):

    context = {
        "images": [
            {"name": "images/quiet.png"}
        ],
        "documents": [
            {"file": "aubin"}
        ]
    }
    return render(request, "schedule/home.html", context)


def history(request):

    response = requests.get(APP_PLANNINGS_BASE_URL)
    context = {
        "history": response.json()
    }
    return render(request, "schedule/history.html", context)


def history_detail(request, id):

    response = requests.get(APP_PLANNINGS_BASE_URL + str(id))
    info = response.json()
    info["activities"] = json.loads(info.get("activities", ""))
    context = {
        "history_info": info
    }
    return render(request, "schedule/history.html", context)


def history_delete(request, id):

    requests.delete(APP_PLANNINGS_BASE_URL + str(id))
    return history(request)


def create_schedule(request):

    context = {}
    if request.method == 'POST':
        activities = []
        req_moods = []
        for key, value in APP_FEELINGS.items():
            if request.POST.get(key):
                req_moods.append(key)
                for i, number in enumerate(value["work"]):
                    activities.extend(number * [APP_ACTIVITIES[i]])
                pto = value.get("pto")
                if pto:
                    activities.extend(pto * ["PTO"])
        activities = activities or (APP_WORKING_HOURS * APP_ACTIVITIES)
        print("activities => {}".format(activities))
        choices = []
        for _ in range(APP_WORKING_HOURS):
            choice = random.choice(activities)
            if choice.lower() == "pto":
                choices = "PTO"
                break
            activities.remove(choice)
            choices.append(choice.upper())
        print("choices => {}".format(choices))
        on_pto = False
        activities = ""
        if choices == "PTO":
            context = {"PTO": True}
            on_pto = True
        else:
            schedule = Counter(choices)
            activities = [{"name": key, "hours": value} for key, value in dict(schedule).items()]
            context = {'Activities': activities}
        requests.post(
            APP_PLANNINGS_BASE_URL,
            json = {
                "activities": json.dumps(activities),
                "pto": on_pto,
                "name": "{0} [{1}]".format(str(datetime.now()), " ".join(req_moods))
            },
        )
        print("context => {0}".format(context))
    return render(request, "schedule/schedule.html", context)