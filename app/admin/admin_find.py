import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View

from app.models import UserProfile, Player_Basic


class Admin_Find(View):
    def __init__(self):
        self.GET = None
        self.user = None
        self.POST = None
        super().__init__()

    def AutoFind(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_addpeople.html', context)

    def CreatePlayer(self):
        username = self.POST.get('username')
        phone = self.POST.get('phone')
        time = self.POST.get('time')
        area = self.POST.get('area')
        school = self.POST.get('school')
        where = self.POST.get('where')
        nowtime = datetime.datetime.now()
        age = int(nowtime.strftime('%Y')) - int(time[:4])
        user = User.objects.filter(username=phone)
        if len(user) == 0:
            user = User.objects.create_user(username=phone, password='123456')
            profile = UserProfile()
            profile.user_id = user.id
            profile.name = username
            profile.palace = area
            profile.role = '球员'
            profile.rights = 4
            profile.date = time
            profile.age = age
            profile.school = school
            profile.save()
            player_basic = Player_Basic()
            player_basic.user_id = profile.id
            player_basic.position = where
            player_basic.where_from = self.user.id
            player_basic.save()
            return HttpResponse('添加成功')
        else:
            return HttpResponse('该手机号已被注册了')

    def CreateRole(self):
        username = self.POST.get('username')
        phone = self.POST.get('phone')
        time = self.POST.get('time')
        area = self.POST.get('area')
        school = self.POST.get('school')
        role = self.POST.get('role')
        nowtime = datetime.datetime.now()
        age = int(nowtime.strftime("%Y")) - int(time[:4])
        user = User.objects.filter(username=phone)
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        if len(user) == 0:
            user = User.objects.create_user(username=phone, password='123456')
            profile = UserProfile()
            profile.user_id = user.id
            profile.name = username
            profile.palace = area
            if role == '教练':
                profile.rights = 2
            else:
                profile.rights = 3
            profile.role = role
            profile.date = time
            profile.age = age
            profile.school = school
            profile.team_id = team_id
            profile.save()
            return HttpResponse('添加成功')
        else:
            return HttpResponse('该手机号码已被注册')
