import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render
from django.views.generic.base import View

from app.admin.return_msg import Msg
from app.models import UserProfile, Team, Schedule, TeamSet, Player_season


class Index(View):
    def __init__(self, **kwargs):
        self.user = None
        self.POST = None
        super().__init__(**kwargs)

    # 后台管理首页
    @login_required
    def sys_min(self):
        try:
            team_id = UserProfile.objects.get(user_id=self.user.id).team_id
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
            teamset = TeamSet.objects.get(team_id=team_id).nowseason
            if len(teamset) == 0:
                all_schedule = Schedule.objects.filter(Q(team_one=team_id) | Q(team_two=team_id))
            else:
                all_schedule = Schedule.objects.filter(Q(team_one=team_id) | Q(team_two=team_id), season_id=teamset)
            all_count = len(all_schedule)
            count = 0
            for i in all_schedule:
                one_score = Player_season.objects.filter(schedule_id=i.id, team_id=Team.objects.get(id=i.team_one).id).aggregate(Sum('score'))['score__sum']
                two_score = Player_season.objects.filter(schedule_id=i.id, team_id=Team.objects.get(id=i.team_two).id).aggregate(Sum('score'))['score__sum']
                one_id = Team.objects.get(id=i.team_one).id
                two_id = Team.objects.get(id=i.team_two).id
                if Msg().Judge(Msg().ReturnNone(one_score), Msg().ReturnNone(two_score), one_id, two_id, team_id) == '胜利':
                    count = count + 1
            context = dict()
            context['date'] = date
            print(date)
            season_date = {'No': 1, 'success': count, 'error': all_count - count, 's_sum': round(count / all_count*100, 2)}
            print(season_date)
            context['team_date'] = team_date
            context['team_one'] = team_one
            context['season_date'] = season_date
            return render(self, 'system_min.html', context)
        except Exception as e:
            print(e)
            return render(self, 'super_login.html')
