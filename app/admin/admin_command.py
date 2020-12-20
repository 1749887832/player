import json
from django.http import JsonResponse
import datetime, time

from django.shortcuts import render
import datetime

from django.views.decorators.csrf import csrf_exempt

from app.admin.return_msg import Msg
from app.models import UserProfile, Command


class Player_Command:
    def __init__(self):
        super().__init__()
        self.POST = None
        self.user = None

    def Show_command(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_command.html', context)

    @csrf_exempt
    def Show_all(self):
        page = int(self.POST.get('page'))
        limit = int(self.POST.get('limit'))
        try:
            team_id = UserProfile.objects.get(user_id=self.user.id).team_id
            command = Command.objects.filter(team_id=team_id)[limit * (page - 1):page * limit]
            count = len(command)
            date = list()
            for i in command:
                context = dict()
                context['id'] = i.id
                context['title'] = i.title
                context['main_player'] = UserProfile.objects.get(id=i.main_player).name
                all_player = ''
                for j in i.player.split(','):
                    if j == '':
                        pass
                    else:
                        all_player = all_player + UserProfile.objects.get(id=j).name + ','
                context['player'] = all_player[:-1]
                context['sum_pass'] = i.sum_pass
                context['sum_pull'] = i.sum_pull
                context['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                context['start_time'] = i.start_time.strftime('%Y-%m-%d') + ' 00:00:00'
                context['end_time'] = i.end_time.strftime('%Y-%m-%d') + ' 23:59:59'
                date.append(context)
            return JsonResponse(Msg().Success(date=date, count=count), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    def C_command(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_createcommand.html', context)

    def Create_command(self):
        print(self.POST)
        title = self.POST.get('title')
        main_player = self.POST.get('main_player')
        time = self.POST.get('time')
        all_player = self.POST.getlist('player[]')
        player = ''
        for i in all_player:
            player = player + str(i) + ','
        sum_pass = self.POST.get('pass')
        sum_pull = self.POST.get('pull')
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time)
        if time == '':
            start_time = '2000-1-1'
            end_time = '2099-12-31'
        else:
            start_time = time.split(' 至 ')[0]
            end_time = time.split(' 至 ')[-1]
        try:
            command = Command.objects.create(
                title=title,
                main_player=main_player,
                player=player,
                sum_pass=sum_pass,
                sum_pull=sum_pull,
                create_time=create_time,
                start_time=start_time,
                end_time=end_time,
                team_id=team_id
            )
            command.save()
            return JsonResponse(Msg().Success(), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
