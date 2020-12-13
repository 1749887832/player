import json

from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from app.models import UserProfile, Player_Basic, Season, Schedule, Team, Player_season, SignUp
from app.admin.return_msg import Msg
import datetime, time
from django.db.models import Avg, Min, Max, Sum, Count


class Record:
    def __init__(self):
        super().__init__()
        self.POST = None
        self.user = None

    def Show_all(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_record.html', context)

    def Select_season(self):
        try:
            season = Season.objects.all()
            data = list()
            for i in season:
                context = dict()
                context['id'] = i.id
                context['name'] = i.name
                data.append(context)
            return JsonResponse(Msg().Success(data), safe=False)
        except Exception:
            return JsonResponse(Msg().Error(), safe=False)

    def Select_players(self):
        season_id = self.POST.get('season_id')
        season_name = Season.objects.filter(id=season_id)
        data = list()
        context = dict()
        context['season_id'] = season_name[0].id
        context['season_name'] = season_name[0].name
        data.append(context)
        try:
            date = UserProfile.objects.get(user_id=self.user.id)
            team_date = Team.objects.get(id=date.team_id)
            player = UserProfile.objects.filter(team_id=team_date.id, rights=4)
            for i in player:
                content = dict()
                content['player_id'] = i.id
                content['player_name'] = i.name
                data.append(content)
            # for i in schedule:
            # print(content)
        except Exception:
            return JsonResponse(Msg().Error(), safe=False)
        # print(data)
        return JsonResponse(Msg().Success(data), safe=False)

    # 查询球员赛程添加数据
    def Select_schedule(self):
        season_id = self.POST.get('season_id')
        player_id = self.POST.get('player_id')
        try:
            date = UserProfile.objects.get(user_id=self.user.id)
            team_date = Team.objects.get(id=date.team_id)
            player = Player_season.objects.filter(player_id=player_id, season_id=season_id)
            # 查询该球员的签约时间
            create_time = SignUp.objects.get(
                user_id=UserProfile.objects.get(id=player_id).user_id).create_time.strftime("%Y-%m-%d %H:%M:%S")
            times = int(time.mktime(time.strptime(create_time, "%Y-%m-%d %H:%M:%S")))
            start_time = datetime.datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
            end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_times = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")))
            """
                判断球员的签约时间是在当前时间之后还是之前，如果是之前，就查询赛程，如果是之后就返回空
            """
            data = list()
            if times - end_times > 0:
                return JsonResponse(Msg().Success(), safe=False)
            else:
                schedule = Schedule.objects.filter(Q(team_one=team_date.id) | Q(team_two=team_date.id),
                                                   season_id=season_id, time__range=[create_time, end_time])
                for i in schedule:
                    if (len(Player_season.objects.filter(player_id=player_id, season_id=season_id,
                                                         schedule_id=i.id)) == 0):
                        content = dict()
                        content['schedule_id'] = i.id
                        content['msg'] = Team.objects.get(id=i.team_one).name + 'VS' + Team.objects.get(
                            id=i.team_two).name + '(' + i.time.strftime('%Y-%m-%d') + '-' + i.type + ')'
                        data.append(content)
                    else:
                        pass
                # print(data)
                return JsonResponse(Msg().Success(data), safe=False)
        except Exception:
            return JsonResponse(Msg().Error(), safe=False)

    # 这是添加球员数据的方法
    def Add_playerdata(self):
        # print(self.POST)
        global add_data
        for i in self.POST:
            add_data = json.loads(i)
        season_id = Schedule.objects.get(id=add_data['schedule_id']).season_id
        # print(season_id)
        # print(add_data['shoot'])
        Msg().ChangMsg(add_data['shoot'])
        # print(Msg().ChangMsg(add_data['shoot']))
        try:
            """
                这里没有判断上场时间的问题，实际情况上上场时间为0不可能有数据(默认情况为0)，然后
                没有判断得分和投篮计算来的得分是否相等的情况，后续改进
            """
            player_data = Player_season.objects.create(
                player_id=add_data['player_id'],
                schedule_id=add_data['schedule_id'],
                time=add_data['time'],
                shoot=Msg().ChangMsg(add_data['shoot']).split('-')[0],
                hit_shoot=Msg().ChangMsg(add_data['shoot']).split('-')[-1],
                three_points=Msg().ChangMsg(add_data['three_points']).split('-')[0],
                hit_points=Msg().ChangMsg(add_data['three_points']).split('-')[-1],
                free_throw=Msg().ChangMsg(add_data['free_throw']).split('-')[0],
                hit_throw=Msg().ChangMsg(add_data['free_throw']).split('-')[-1],
                assists=add_data['assists'],
                all_court=float(add_data['front_court']) + float(add_data['back_court']),
                front_court=add_data['front_court'],
                back_court=add_data['back_court'],
                block_shot=add_data['block_shot'],
                snatch=add_data['snatch'],
                error=add_data['error'],
                break_rules=add_data['break_rules'],
                season_id=season_id,
                score=add_data['score'],
                team_id=UserProfile.objects.get(user_id=self.user.id).team_id
            )
            player_data.save()
            return JsonResponse(Msg().Success(), safe=False)
        except Exception:
            return JsonResponse(Msg().Error(), safe=False)

    @csrf_exempt
    def Record_show(self):
        # 获取到team_id
        # print(self.POST.get('main_season'))
        # print(self.POST.get('main_player'))
        page = int(self.POST.get('page'))
        limit = int(self.POST.get('limit'))
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        player_data = list()
        name = self.POST.get('main_title')
        # print(name)
        all_player = UserProfile.objects.filter(team_id=team_id, rights=4, role='球员',
                                                id__icontains=self.POST.get('main_player'),
                                                name__icontains=self.POST.get('main_title'))[
                     limit * (page - 1):page * limit]
        count = len(all_player)
        # print(count)
        """
            这里返回数据和逻辑有点混乱，后期改进
        """
        try:
            for i in all_player:
                # 获取球队中的球员id
                # print(i.id)
                player = Player_season.objects.filter(player_id=i.id)
                if self.POST.get('main_player') != '':
                    player = Player_season.objects.filter(player_id=i.id,
                                                          season_id__contains=self.POST.get('main_season'))
                    for j in player:
                        player_context = dict()
                        player_context['id'] = j.id
                        player_context['name'] = i.name
                        player_context['battle'] = Team.objects.get(
                            id=Schedule.objects.get(id=j.schedule_id).team_one).name + ' VS ' + Team.objects.get(
                            id=Schedule.objects.get(id=j.schedule_id).team_two).name
                        player_context['score'] = j.score
                        player_context['time'] = j.time
                        player_context['shoot'] = str(j.shoot) + "-" + str(j.hit_shoot)
                        player_context['hit'] = 0.0 if j.shoot == '0' else round(
                            (int(j.hit_shoot) / int(j.shoot)) * 100, 2)
                        player_context['three_points'] = str(j.three_points) + '-' + str(j.hit_points)
                        player_context['three_hit'] = 0.0 if j.three_points == '0' else round(
                            int(j.hit_points) / int(j.three_points) * 100, 2)
                        player_context['free_throw'] = str(j.free_throw) + '-' + str(j.hit_throw)
                        player_context['hit_throw'] = 0.0 if j.free_throw == '0' else round(
                            int(j.hit_throw) / int(j.free_throw) * 100, 2)
                        player_context['all_court'] = j.all_court
                        player_context['front_court'] = j.front_court
                        player_context['back_court'] = j.back_court
                        player_context['assists'] = j.assists
                        player_context['snatch'] = j.snatch
                        player_context['block_shot'] = j.block_shot
                        player_context['error'] = j.error
                        player_context['break_rules'] = j.break_rules
                        player_data.append(player_context)
                        # print(player_context)
                else:
                    sum = Player_season.objects.filter(player_id=i.id,
                                                       season_id__contains=self.POST.get('main_season')).aggregate(
                        Avg('score'), Avg('time'), Sum('shoot'), Avg('shoot'), Avg('three_points'), Avg('free_throw'),
                        Sum('hit_shoot'), Sum('three_points'), Sum('hit_points'), Sum('free_throw'), Sum('hit_throw'),
                        Avg('front_court'), Avg('back_court'), Avg('assists'), Avg('snatch'), Avg('block_shot'),
                        Avg('error'), Avg('break_rules'), Avg('all_court'))
                    # print(sum)
                    # print(sum)
                    player_context = dict()
                    # 学生id
                    player_context['id'] = i.id
                    # 学生姓名
                    player_context['name'] = i.name
                    player_context['battle'] = ''
                    # 平均得分
                    player_context['score'] = round(Msg().ReturnNone(sum['score__avg']), 2)
                    # 平均上场时间
                    player_context['time'] = round(Msg().ReturnNone(sum['time__avg']), 2)
                    # 平均出手次数
                    player_context['shoot'] = round(Msg().ReturnNone(sum['shoot__avg']), 2)
                    # 命中率
                    player_context['hit'] = 0.0 if Msg().ReturnNone(sum['hit_shoot__sum']) == 0 else round(
                        Msg().ReturnNone(sum['hit_shoot__sum']) / Msg().ReturnNone(sum['shoot__sum']) * 100, 2)
                    # 三分出手次数
                    player_context['three_points'] = round(Msg().ReturnNone(sum['three_points__avg']), 2)
                    # 三分命中率
                    player_context['three_hit'] = 0.0 if Msg().ReturnNone(sum['hit_points__sum']) == 0 else round(
                        Msg().ReturnNone(sum['hit_points__sum']) / Msg().ReturnNone(sum['three_points__sum']) * 100, 2)
                    # 罚球次数
                    player_context['free_throw'] = round(Msg().ReturnNone(sum['free_throw__avg']), 2)
                    # 罚球命中率
                    player_context['hit_throw'] = 0.0 if Msg().ReturnNone(sum['hit_throw__sum']) == 0 else round(
                        Msg().ReturnNone(sum['hit_throw__sum']) / Msg().ReturnNone(sum['free_throw__sum']) * 100, 2)
                    # 平均篮板
                    player_context['all_court'] = round(Msg().ReturnNone(sum['all_court__avg']), 2)
                    # 平均前场篮板
                    player_context['front_court'] = round(Msg().ReturnNone(sum['front_court__avg']), 2)
                    # 平均后场篮板
                    player_context['back_court'] = round(Msg().ReturnNone(sum['back_court__avg']), 2)
                    # 平均助攻数
                    player_context['assists'] = round(Msg().ReturnNone(sum['assists__avg']), 2)
                    # 平均盖帽
                    player_context['snatch'] = round(Msg().ReturnNone(sum['snatch__avg']), 2)
                    # 平均抢断
                    player_context['block_shot'] = round(Msg().ReturnNone(sum['block_shot__avg']), 2)
                    # 平均失误
                    player_context['error'] = round(Msg().ReturnNone(sum['error__avg']), 2)
                    # 平均犯规
                    player_context['break_rules'] = round(Msg().ReturnNone(sum['break_rules__avg']), 2)
                    # print(player_context)
                    player_data.append(player_context)
            return JsonResponse(Msg().Success(date=player_data, count=count), safe=False)
        except Exception:
            return JsonResponse(Msg().Error(), safe=False)

    # 比较两个球队的得分，然后得出结果
    def Judge(self, one_score, two_score, one_id, two_id, you_id):
        if one_score > two_score:
            if one_id == you_id:
                return "胜利"
            else:
                return "失败"
        elif one_score < two_score:
            if two_id == you_id:
                return "胜利"
            else:
                return "失败"
        else:
            return "平局"

    @csrf_exempt
    def Show_teamrecord(self):
        page = self.POST.get('page')
        limit = self.POST.get('limit')
        team_title = self.POST.get('team_title')
        all_team = self.POST.get('all_team')
        all_season = self.POST.get('all_season')
        all_type = self.POST.get('all_type')
        # print(team_title, all_team, all_season, all_type)
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        # 查询该赛季下的赛程
        all_data = Player_season.objects.filter(team_id=team_id, season_id=1)
        if all_team == '':
            all_schedule = Schedule.objects.filter(Q(team_one=team_id) | Q(team_two=team_id),
                                                   season_id__icontains=all_season, type__icontains=all_type)
        else:
            all_schedule = Schedule.objects.filter(
                (Q(team_one=team_id) | Q(team_two=team_id)) & (Q(team_one=all_team) | Q(
                    team_two=all_team)), season_id__icontains=all_season, type__icontains=all_type)
        # print(all_schedule.query)
        count = len(all_schedule)
        data = list()
        for i in all_schedule:
            # all_schedule = Schedule.objects.get(id=i.schedule_id)
            context = dict()
            context['id'] = i.id
            # 第一个球队
            one_id = Team.objects.get(id=i.team_one).id
            context['team_one'] = Team.objects.get(id=i.team_one).name
            # 球队的图片
            context['team_onepic'] = Team.objects.get(id=i.team_one).team_pic
            # 球场
            context['team_area'] = Team.objects.get(id=i.team_one).aarea
            # 第二个球队
            two_id = Team.objects.get(id=i.team_two).id
            context['team_two'] = Team.objects.get(id=i.team_two).name
            # 第二个球队的图片
            context['team_twopic'] = Team.objects.get(id=i.team_two).team_pic
            # 类型
            context['type'] = Schedule.objects.get(id=i.id).type
            # 获取开赛时间
            context['time'] = Schedule.objects.get(id=i.id).time.strftime('%Y-%m-%d %H:%M:%S')
            # 第一个球队的得分
            one_score = \
                Player_season.objects.filter(schedule_id=i.id, team_id=Team.objects.get(id=i.team_one).id).aggregate(
                    Sum('score'))['score__sum']
            context['one_score'] = Msg().ReturnNone(one_score)
            # 第二个球队的得分
            two_score = \
                Player_season.objects.filter(schedule_id=i.id, team_id=Team.objects.get(id=i.team_two).id).aggregate(
                    Sum('score'))['score__sum']
            context['two_score'] = Msg().ReturnNone(two_score)
            # 结果
            context['result'] = Record().Judge(context['one_score'], context['two_score'], one_id, two_id, team_id)
            data.append(context)
            # print(context)
        return JsonResponse(Msg().Success(date=data,count=count), safe=False)

    # 对比球队数据
    def Team_contrast(self):
        # print(self.POST.get('schedule_id'))
        schedule_id = self.POST.get('schedule_id')
        schedule = Schedule.objects.get(id=schedule_id)
        team_left = schedule.team_one
        team_right = schedule.team_two
        season_id = schedule.season_id
        player_season = Player_season.objects.filter(id=1).values()
        left_data = list()
        right_data = list()
        come_in = ['id', 'time', 'player_id', 'season_id', 'schedule_id', 'team_id']
        for key, value in player_season[0].items():
            if key not in come_in:
                data_left = dict()
                data_right = dict()
                data_left['name'] = key
                data_right['name'] = key
                # print(team_left,season_id)
                left_sum = round(Msg().ReturnNone(float(Msg().ReturnNone(
                    Player_season.objects.filter(schedule_id=schedule_id, team_id=team_left,
                                                 season_id=season_id).aggregate(Sum(key))[key + '__sum']))), 2)
                right_sum = round(Msg().ReturnNone(float(Msg().ReturnNone(
                    Player_season.objects.filter(schedule_id=schedule_id, team_id=team_right,
                                                 season_id=season_id).aggregate(Sum(key))[key + '__sum']))), 2)
                if key in ['hit_shoot', 'hit_throw', 'hit_points']:
                    left_count = Msg().Count_pro(left_sum, left_data[-1]['value'])
                    right_count = Msg().Count_pro(right_sum, right_data[-1]['value'])
                    data_left['value'] = str(left_count) + '%'
                    data_right['value'] = str(right_count) + '%'
                    data_left['percent'] = str(Msg().Count_pro(left_count, right_count)) + '%'
                    data_right['percent'] = '0%' if left_count == 0.0 and right_count == 0.0 else str(
                        100 - Msg().Count_pro(left_count, right_count)) + '%'
                else:
                    data_left['value'] = left_sum
                    data_right['value'] = right_sum
                    # print(left_sum+right_sum)
                    data_left['percent'] = str(Msg().Count_pro(left_sum, right_sum)) + '%'
                    data_right['percent'] = '0%' if left_sum == 0.0 and right_sum == 0.0 else str(
                        100 - Msg().Count_pro(left_sum, right_sum)) + '%'
                    # print(data_left,data_right)
                left_data.append(data_left)
                right_data.append(data_right)
            else:
                pass
        return JsonResponse(Msg().Success([left_data, right_data]), safe=False)

    # 查询球队
    def Select_team(self):
        all_team = Team.objects.exclude(id=1)
        data = list()
        for i in all_team:
            context = dict()
            context['id'] = i.id
            context['name'] = i.name
            data.append(context)
        return JsonResponse(Msg().Success(data), safe=False)
