from django.shortcuts import render

import os
import random
from collections import Counter


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
    "annoyed": {"work": [5, 0, 0, 0, 10, 10, 10], "pto": 1},
    "bored": {"work": [5, 10, 0, 0, 5, 0, 5], "pto": 1},
    "cool": {"work": [0, 10, 10, 10, 10, 0, 0]},
    "hot": {"work": [5, 5, 5, 5, 0, 2, 5], "pto": 1},
    "nervous": {"work": [10, 5, 2, 0, 0, 0, 5], "pto": 1},
    "quiet": {"work": [5, 10, 0, 0, 0, 0, 10]},
    "sick": {"work": [0, 0, 0, 0, 0, 0, 0], "pto": 10},
    "sleep": {"work": [5, 1, 0, 0, 5, 0, 0], "pto": 2},
}

APP_WORKING_HOURS = 8


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


def create_schedule(request):

    context = {}
    if request.method == 'POST':
        activities = []
        for key, value in APP_FEELINGS.items():
            if request.POST.get(key):
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
        if choices == "PTO":
            context = {"PTO": True}
        else:
            schedule = Counter(choices)
            context = {'Activities': [{"name": key, "hours": value} for key, value in dict(schedule).items()]}
        print("context => {0}".format(context))
    return render(request, "schedule/schedule.html", context)