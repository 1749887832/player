import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

from app.models import UserProfile, Team, Schedule


class Index(View):
    def __init__(self, **kwargs):
        self.user = None
        self.POST = None
        super().__init__(**kwargs)

    # 后台管理首页
    @login_required
    def sys_min(self):
        date = UserProfile.objects.get(user_id=self.user.id)
        team_date = Team.objects.get(id=date.team_id)
        time = datetime.datetime.now()
        # 查询比赛日期
        team_one = Schedule.objects.filter(Q(team_one=team_date.id) | Q(team_two=team_date.id),
                                           time__year=time.strftime('%Y'), time__month=time.strftime('%m'),
                                           time__day=time.strftime('%d'))
        for i in team_one:
            i.team_one = Team.objects.get(id=i.team_one)
            i.team_two = Team.objects.get(id=i.team_two)
            if i.team_one.name == team_date.name:
                i.home = '主'
            else:
                i.home = '客'
        context = dict()
        context['date'] = date
        context['team_date'] = team_date
        context['team_one'] = team_one
        return render(self, 'system_min.html', context)

