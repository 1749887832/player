import json

from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.admin.return_msg import Msg
from app.models import UserProfile, Team, TeamSet, Player_Basic, Player_season, Season


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

    def Show_money(self):
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        msg = TeamSet.objects.filter(team_id=team_id)
        date = list()
        context = dict()
        if len(msg) == 0:
            context['money'] = 0
            context['max_money'] = 0
            date.append(context)
            return JsonResponse(Msg().Success(date=date), safe=False)
        else:
            context['money'] = Msg().ReturnNone(msg[0].money)
            context['max_money'] = Msg().ReturnNone(msg[0].max_money)
            date.append(context)
            return JsonResponse(Msg().Success(date=date), safe=False)

    def Update_money(self):
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        date = TeamSet.objects.filter(team_id=team_id)
        try:
            if len(date) == 0:
                teamset = TeamSet.objects.create(
                    team_id=team_id,
                    money=self.POST.get('money'),
                    max_money=self.POST.get('max_money')
                )
                teamset.save()
                return JsonResponse(Msg().Success(), safe=False)
            else:
                TeamSet.objects.filter(team_id=team_id).update(
                    money=self.POST.get('money'),
                    max_money=self.POST.get('max_money')
                )
                return JsonResponse(Msg().Success(), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    @csrf_exempt
    def Show_roles(self):
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        data = TeamSet.objects.filter(team_id=team_id)
        date = list()
        msg = ['pg', 'sg', 'sf', 'pf', 'c']
        msg_date = ['控球后卫', '得分后卫', '小前锋', '大前锋', '中锋']
        try:
            if len(data) == 0:
                context = dict()
                for i in msg:
                    context['postion'] = msg_date[msg.index(i)]
                    date.append(context)
                return JsonResponse(Msg().Success(date=date), safe=False)
            else:
                num = TeamSet.objects.get(team_id=team_id)
                for i in msg:
                    content = dict()
                    if i == 'pg':
                        a = num.pg
                    elif i == 'sg':
                        a = num.sg
                    elif i == 'sf':
                        a = num.sf
                    elif i == 'pf':
                        a = num.pf
                    else:
                        a = num.c
                    content['postion'] = msg_date[msg.index(i)]
                    if a is not None and a != '':
                        content['setid'] = i
                        content['id'] = UserProfile.objects.get(id=a).id
                        content['name'] = UserProfile.objects.get(id=a).name
                        content['age'] = UserProfile.objects.get(id=a).age
                        content['rolepostion'] = Player_Basic.objects.get(user_id=UserProfile.objects.get(id=a).id).position
                        content['time'] = round(Msg().ReturnNone(Player_season.objects.filter(player_id=a).aggregate(Avg('time'))['time__avg']), 2)
                        content['score'] = round(Msg().ReturnNone(Player_season.objects.filter(player_id=a).aggregate(Avg('score'))['score__avg']), 2)
                        content['assists'] = round(Msg().ReturnNone(Player_season.objects.filter(player_id=a).aggregate(Avg('assists'))['assists__avg']), 2)
                        content['court'] = round(Msg().ReturnNone(Player_season.objects.filter(player_id=a).aggregate(Avg('all_court'))['all_court__avg']), 2)
                        content['snatch'] = round(Msg().ReturnNone(Player_season.objects.filter(player_id=a).aggregate(Avg('snatch'))['snatch__avg']), 2)
                        content['block_shot'] = round(Msg().ReturnNone(Player_season.objects.filter(player_id=a).aggregate(Avg('block_shot'))['block_shot__avg']), 2)
                    else:
                        pass
                    date.append(content)
        except Exception as e:
            # 打印日志报错
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
        return JsonResponse(Msg().Success(date=date), safe=False)

    def Del_roles(self):
        msg = self.POST.get('setid')
        try:
            team_id = UserProfile.objects.get(user_id=self.user.id).team_id
            if msg == 'pg':
                TeamSet.objects.filter(team_id=team_id).update(pg='')
            elif msg == 'sg':
                TeamSet.objects.filter(team_id=team_id).update(sg='')
            elif msg == 'sf':
                TeamSet.objects.filter(team_id=team_id).update(sf='')
            elif msg == 'pf':
                TeamSet.objects.filter(team_id=team_id).update(pf='')
            elif msg == 'c':
                TeamSet.objects.filter(team_id=team_id).update(c='')
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
        return JsonResponse(Msg().Success(), safe=False)

    @csrf_exempt
    def Show_season(self):
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        try:
            season = Season.objects.all()
            now_season = TeamSet.objects.filter(team_id=team_id)
            date = list()
            if len(now_season) == 0 or now_season[0].nowseason is None:
                nowseason = None
            else:
                nowseason = now_season[0].nowseason
            for i in season:
                context = dict()
                context['id'] = i.id
                if str(i.id) == nowseason:
                    context['is_now'] = 'true'
                else:
                    context['is_now'] = 'false'
                context['name'] = i.name
                date.append(context)
            return JsonResponse(Msg().Success(date), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    def Set_nowseason(self):
        season_id = self.POST.get('season_id')
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        try:
            TeamSet.objects.filter(team_id=team_id).update(
                nowseason=season_id
            )
            return JsonResponse(Msg().Success(), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    def Update_setplayers(self):
        postion = self.POST.get('postion')
        player_id = self.POST.get('player_id')
        try:
            team_id = UserProfile.objects.get(user_id=self.user.id).team_id
            if postion == '控球后卫':
                TeamSet.objects.filter(team_id=team_id).update(pg=player_id)
            elif postion == '得分后卫':
                TeamSet.objects.filter(team_id=team_id).update(sg=player_id)
            elif postion == '小前锋':
                TeamSet.objects.filter(team_id=team_id).update(sf=player_id)
            elif postion == '大前锋':
                TeamSet.objects.filter(team_id=team_id).update(pf=player_id)
            elif postion == '中锋':
                TeamSet.objects.filter(team_id=team_id).update(c=player_id)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
        return JsonResponse(Msg().Success(), safe=False)
