from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from app.models import UserProfile, Player_Basic


class Record:
    def __init__(self):
        super().__init__()
        self.user = None

    def Show_all(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_record.html', context)
