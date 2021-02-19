import json
from django.http import JsonResponse
import datetime, time

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.admin.return_msg import Msg
from app.models import UserProfile, SignUp, TeamSet, Season


class Finance:
    def __init__(self):
        super().__init__()
        self.POST = None
        self.user = None

    def Show_finance(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_finance.html', context)

    @csrf_exempt
    def Show_playerfinance(self):
        page = int(self.POST.get('page'))
        limit = int(self.POST.get('limit'))
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        all_player = UserProfile.objects.filter(team_id=team_id, rights=4, role='球员')[limit * (page - 1):page * limit]
        count = len(all_player)
        date = list()
        try:
            for i in all_player:
                context = dict()
                context['id'] = i.user_id
                context['name'] = i.name
                context['userpic'] = i.userpic
                context['age'] = i.age
                context['sex'] = i.sex
                money = SignUp.objects.get(user_id=i.user_id).money
                context['money'] = money
                context['p_chance'] = SignUp.objects.get(user_id=i.user.id).p_chance
                year = SignUp.objects.get(user_id=i.user.id).year
                for j in range(int(year)):
                    if j != int(year) - 1:
                        context['year' + str(j)] = round(int(money) / year, 2)
                    else:
                        context['year' + str(j)] = round(int(money) - round(int(money) / year, 2) * (int(year - 1)), 2)

                context['time'] = SignUp.objects.get(user_id=i.user.id).create_time.strftime('%Y-%m-%d')
                context['type'] = SignUp.objects.get(user_id=i.user.id).type
                context['p_year'] = SignUp.objects.get(user_id=i.user.id).p_year
                date.append(context)
            return JsonResponse(Msg().Success(date=date, count=count), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    def Count_money(self):
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        teamset = TeamSet.objects.filter(team_id=team_id)
        try:
            date = list()
            context = dict()
            if len(teamset) == 0:
                context['nowseason'] = ''
                context['player_money'] = 0.0
                context['exceed_money'] = 0.0
                context['real_money'] = 0.0
                date.append(context)
            else:
                context['nowseason'] = Season.objects.get(id=TeamSet.objects.get(team_id=team_id).nowseason).name
                money = Msg().ReturnNone(TeamSet.objects.get(team_id=team_id).money)
                max_money = Msg().ReturnNone(TeamSet.objects.get(team_id=team_id).max_money)
                all_player = UserProfile.objects.filter(team_id=team_id, rights=4, role='球员')
                count_money = 0
                for i in all_player:
                    year = int(SignUp.objects.get(user_id=i.user_id).year)
                    creata_time = int(SignUp.objects.get(user_id=i.user.id).create_time.strftime("%Y"))
                    nowseason_time = int(context['nowseason'].split('-')[0])
                    if creata_time <= nowseason_time <= creata_time + year:
                        count_money = count_money + round(int(SignUp.objects.get(user_id=i.user_id).money) / year, 2)
                        # print(count_money)
                context['player_money'] = count_money
                if count_money > int(money):
                    context['exceed_money'] = count_money - int(money)
                    context['real_money'] = round(count_money + context['exceed_money'] * 2, 2)
                else:
                    context['exceed_money'] = 0.0
                    context['real_money'] = round(count_money, 2)
                date.append(context)
            return JsonResponse(Msg().Success(date=date), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
