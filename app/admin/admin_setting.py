import json
from django.http import JsonResponse
import datetime, time

from django.shortcuts import render

from app.models import UserProfile


class Setting:
    def __init__(self):
        super().__init__()
        self.POST = None
        self.user = None

    def Show_setting(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_setting.html', context)
