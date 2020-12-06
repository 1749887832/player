import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from app.models import UserProfile, Player_Basic, Season, Schedule, Team, Player_season, SignUp
from app.admin.return_msg import Msg
import datetime, time


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
        print(data)
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

    def Add_playerdata(self):
        print(self.POST)
        global add_data
        for i in self.POST:
            add_data = json.loads(i)
        season_id = Schedule.objects.get(id=add_data['schedule_id']).season_id
        print(season_id)
        print(add_data['shoot'])
        Msg().ChangMsg(add_data['shoot'])
        print(Msg().ChangMsg(add_data['shoot']))
        try:
            """
                这里没有判断上场时间的问题，实际情况上上场时间为0不可能有数据(默认情况为0)，然后
                没有判断得分和投篮计算来的得分是否相等的情况，后续改进
            """
            player_data = Player_season.objects.create(
                player_id=add_data['player_id'],
                schedule_id=add_data['schedule_id'],
                time=add_data['time'],
                shoot=Msg().ChangMsg(add_data['shoot']),
                three_points=Msg().ChangMsg(add_data['three_points']),
                free_throw=Msg().ChangMsg(add_data['free_throw']),
                assists=add_data['assists'],
                front_court=add_data['front_court'],
                back_court=add_data['back_court'],
                block_shot=add_data['block_shot'],
                snatch=add_data['snatch'],
                error=add_data['error'],
                break_rules=add_data['break_rules'],
                season_id=season_id,
                score=add_data['score']
            )
            player_data.save()
            return JsonResponse(Msg().Success(), safe=False)
        except Exception:
            return JsonResponse(Msg().Error(), safe=False)

    def Record_show(self):
        data = {
            "status": 200
            , "message": ""
            , "total": 8
            , "rows": {
                "item": [{
                    "id": "10001"
                    , "username": "杜甫"
                    , "email": "xianxin@layui.com"
                    , "sex": "男"
                    , "city": "浙江杭州"
                    , "sign": "点击此处，显示更多。当内容超出时，点击单元格会自动显示更多内容。"
                    , "experience": "116"
                    , "ip": "192.168.0.8"
                    , "logins": "108"
                    , "joinTime": "2016-10-14"
                }, {
                    "id": "10002"
                    , "username": "李白"
                    , "email": "xianxin@layui.com"
                    , "sex": "男"
                    , "city": "浙江杭州"
                    ,
                    "sign": "君不见，黄河之水天上来，奔流到海不复回。 君不见，高堂明镜悲白发，朝如青丝暮成雪。 人生得意须尽欢，莫使金樽空对月。 天生我材必有用，千金散尽还复来。 烹羊宰牛且为乐，会须一饮三百杯。 岑夫子，丹丘生，将进酒，杯莫停。 与君歌一曲，请君为我倾耳听。(倾耳听 一作：侧耳听) 钟鼓馔玉不足贵，但愿长醉不复醒。(不足贵 一作：何足贵；不复醒 一作：不愿醒/不用醒) 古来圣贤皆寂寞，惟有饮者留其名。(古来 一作：自古；惟 通：唯) 陈王昔时宴平乐，斗酒十千恣欢谑。 主人何为言少钱，径须沽取对君酌。 五花马，千金裘，呼儿将出换美酒，与尔同销万古愁。"
                    , "experience": "12.25"
                    , "ip": "192.168.0.8"
                    , "logins": "106"
                    , "joinTime": "2016-10-14"
                }, {
                    "id": "10003"
                    , "username": "王勃"
                    , "email": "xianxin@layui.com"
                    , "sex": "男"
                    , "city": "浙江杭州"
                    , "sign": "人生恰似一场修行"
                    , "experience": "65"
                    , "ip": "192.168.0.8"
                    , "logins": "106"
                    , "joinTime": "2016-10-14"
                }, {
                    "id": "10004"
                    , "username": "李清照"
                    , "email": "xianxin@layui.com"
                    , "sex": "女"
                    , "city": "浙江杭州"
                    , "sign": "人生恰似一场修行"
                    , "experience": "666"
                    , "ip": "192.168.0.8"
                    , "logins": "106"
                    , "joinTime": "2016-10-14"
                }, {
                    "id": "10005"
                    , "username": "冰心"
                    , "email": "xianxin@layui.com"
                    , "sex": "女"
                    , "city": "浙江杭州"
                    , "sign": "人生恰似一场修行"
                    , "experience": "86.05"
                    , "ip": "192.168.0.8"
                    , "logins": "106"
                    , "joinTime": "2016-10-14"
                }, {
                    "id": "10006"
                    , "username": "贤心"
                    , "email": "xianxin@layui.com"
                    , "sex": "男"
                    , "city": "浙江杭州"
                    , "sign": "人生恰似一场修行"
                    , "experience": "12"
                    , "ip": "192.168.0.8"
                    , "logins": "106"
                    , "joinTime": "2016-10-14"
                }, {
                    "id": "10007"
                    , "username": "贤心"
                    , "email": "xianxin@layui.com"
                    , "sex": "男"
                    , "city": "浙江杭州"
                    , "sign": "人生恰似一场修行"
                    , "experience": "16"
                    , "ip": "192.168.0.8"
                    , "logins": "106"
                    , "joinTime": "2016-10-14"
                }, {
                    "id": "10008"
                    , "username": "贤心"
                    , "email": "xianxin@layui.com"
                    , "sex": "男"
                    , "city": "浙江杭州"
                    , "sign": "人生恰似一场修行"
                    , "experience": "106"
                    , "ip": "192.168.0.8"
                    , "logins": "106"
                    , "joinTime": "2016-10-14"
                }]
            }
        }
        return JsonResponse(data, safe=False)
