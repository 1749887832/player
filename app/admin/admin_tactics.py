import json
import os
import time
import uuid

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from app.models import UserProfile, Player_Basic, Tactics, Team
from django.views.decorators.csrf import csrf_exempt
from app.admin.return_msg import Msg
import datetime

picurl = ''


class P_Tactics:
    def __init__(self):
        self.FILES = None
        self.POST = None
        self.GET = None
        self.user = None
        super().__init__()

    def Show_all(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_tactics.html', context)

    # 查询所有的战术
    @csrf_exempt
    def Data(self):
        # print(self.POST)
        # print(self.GET.get('page'))
        page = int(self.POST.get('page'))
        limit = int(self.POST.get('limit'))
        title = Msg().ReNone(self.POST.get('main_title'))
        main_player = Msg().ReNone(self.POST.get('main_player'))
        start_player = Msg().ReNone(self.POST.get('start_player'))
        end_player = Msg().ReNone(self.POST.get('end_player'))
        time = self.POST.get('time')
        if time == '':
            time = '0001-1-1 至 9999-12-31'
        times = time.split('至')
        start_time = datetime.datetime(year=int(times[0].split('-')[0]), month=int(times[0].split('-')[1]),
                                       day=int(times[0].split('-')[2]), hour=0, minute=0, second=0)
        end_time = datetime.datetime(year=int(times[1].split('-')[0]), month=int(times[1].split('-')[1]),
                                     day=int(times[1].split('-')[2]), hour=0, minute=0, second=0)
        # print(self.GET.get('limit'))
        try:
            user = UserProfile.objects.get(user_id=self.user.id)
            team_id = user.team_id
            tactics = Tactics.objects.filter(team_id=team_id, title__contains=title, main_player__contains=main_player,
                                             start_player__contains=start_player, end_player__contains=end_player,
                                             create_time__range=[start_time, end_time])[
                      limit * (page - 1):page * limit]
            count = len(Tactics.objects.filter(team_id=team_id))
            data = list()
            for i in tactics:
                context = dict()
                context['id'] = i.id
                context['title'] = i.title
                context['context'] = i.context
                context['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                context['team'] = Team.objects.filter(id=i.team_id)[0].name
                context['main_player'] = UserProfile.objects.filter(id=i.main_player)[0].name
                context['start_player'] = UserProfile.objects.filter(id=i.start_player)[0].name
                context['end_player'] = UserProfile.objects.filter(id=i.end_player)[0].name
                context['create_user'] = UserProfile.objects.filter(user_id=i.create_user)[0].name
                context['update_user'] = UserProfile.objects.filter(user_id=i.update_uer)[0].name
                data.append(context)
            # print(data)
        except Exception:
            return JsonResponse(Msg().Error('查询失败'), safe=False)
        return JsonResponse(Msg().Success(date=data, count=count), safe=False)

    # 跳转到新建战术页面
    def Create_tatics(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_createtactics.html', context)

    # 查询教练的接口
    def Select_coach(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        team_id = user.team_id
        try:
            coach = UserProfile.objects.filter(team_id=team_id, rights=2)
            data = list()
            for i in coach:
                context = dict()
                context['id'] = i.id
                context['name'] = i.name
                data.append(context)
            # print(data)
            return JsonResponse(Msg().Success(data), safe=False)
        except Exception:
            return JsonResponse(Msg().Error('查询教练失败'), safe=False)

    # 查询球员的接口
    def Select_player(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        team_id = user.team_id
        try:
            player = UserProfile.objects.filter(team_id=team_id, rights=4)
            data = list()
            for i in player:
                context = dict()
                context['id'] = i.id
                context['name'] = i.name
                data.append(context)
            # print(data)
            return JsonResponse(Msg().Success(data), safe=False)
        except Exception:
            return JsonResponse(Msg().Error('查询球员失败'), safe=False)

    # 创建新的战术
    def Create_tatic(self):
        global data
        for i in self.POST:
            data = json.loads(i)
        global picurl
        user = UserProfile.objects.get(user_id=self.user.id)
        team_id = user.team_id
        try:
            tactics = Tactics.objects.create(
                title=data['title'],
                main_player=data['main_player'],
                start_player=data['start_player'],
                end_player=data['end_player'],
                file=picurl,
                context=data['context'],
                create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                create_user=self.user.id,
                update_uer=self.user.id,
                team_id=team_id,
            )
            tactics.save()
        except Exception:
            return JsonResponse(Msg().Error('写入数据库失败'), safe=False)
        return redirect('/player/tactics/')

    # 删除战术
    def Del_tatics(self):
        global context
        for i in self.POST:
            # print(i)
            context = i[1:len(i) - 1].strip(',').split(',')
        try:
            for i in context:
                Tactics.objects.filter(id=i).update(team_id=0)
        except Exception:
            return JsonResponse(Msg().Error('删除数据失败'), safe=False)
        return JsonResponse(Msg().Success(), safe=False)

    # 上传图片到服务
    @csrf_exempt
    def Create_pic(self):
        # print(type(self.FILES.get('file')))
        pic = self.FILES.get('file')
        picName = pic.name
        picStuff = os.path.splitext(picName)[1]
        picUUIDname = str(uuid.uuid1()) + picStuff
        # 设置文件上传到服务器的路径
        uploadDirPath = os.path.join(os.getcwd(), 'app' + os.sep + 'static' + os.sep + 'image')
        # 设置上传文件的绝对路径
        picAbsPath = uploadDirPath + os.sep + picUUIDname
        global picurl
        picurl = 'image/' + picUUIDname
        # 写出二进制数据到文件中
        try:
            with open(picAbsPath, 'wb+')as fp:
                # 对文件进行分块处理
                for chunk in pic.chunks():
                    fp.write(chunk)
        except:
            return JsonResponse(Msg().Error('图片上传失败'), safe=False)
        return JsonResponse(Msg().Success(), safe=False)

    # 查询标题详情接口
    def Title_context(self):
        title_id = self.POST.get('title_id')
        try:
            tactics = Tactics.objects.filter(id=title_id)
            data = list()
            for i in tactics:
                context = dict()
                context['id'] = i.id
                context['title'] = i.title
                context['main_player'] = UserProfile.objects.filter(id=i.main_player)[0].name
                context['start_player'] = UserProfile.objects.filter(id=i.start_player)[0].name
                context['end_player'] = UserProfile.objects.filter(id=i.end_player)[0].name
                context['file'] = i.file
                context['context'] = i.context
                context['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                data.append(context)
        except Exception:
            return JsonResponse(Msg().Error('战术查询失败'), safe=False)
        return JsonResponse(Msg().Success(data), safe=False)

    # 查询战术标题接口
    # def Select_title(self):
    #     user = UserProfile.objects.get(user_id=self.user.id)
    #     team_id = user.team_id
    #     title = Tactics.objects.filter(team_id=team_id)
    #     data = list()
    #     try:
    #         for i in title:
    #             context = dict()
    #             context['title'] = i.title
    #             data.append(context)
    #     except Exception:
    #         return JsonResponse(Msg().Error('标题查询失败'), safe=False)
    #     return JsonResponse(Msg().Success(data), safe=False)
    def Update_tatics(self):
        global number
        number = self.GET.get('number')
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_updatetactics.html', context)

    #  查询接口回显
    def P_tatics(self):
        global number
        try:
            tactics = Tactics.objects.filter(id=number)
            data = list()
            for i in tactics:
                context = dict()
                context['id'] = i.id
                context['title'] = i.title
                context['main_player'] = i.main_player
                context['start_player'] = i.start_player
                context['end_player'] = i.end_player
                context['file'] = i.file
                context['context'] = i.context
                context['create_time'] = i.create_time.strftime('%Y-%m-%d %H:%M:%S')
                data.append(context)
        except Exception:
            return JsonResponse(Msg().Error('战术查询失败'), safe=False)
        return JsonResponse(Msg().Success(data), safe=False)

    # 修改战术接口
    def Update_tatic(self):
        # print(self.POST)
        global number
        global update_data
        for i in self.POST:
            update_data = json.loads(i)
        try:
            Tactics.objects.filter(id=number).update(
                title=update_data['title'],
                main_player=update_data['main_player'],
                start_player=update_data['start_player'],
                end_player=update_data['end_player'],
                file=picurl,
                context=update_data['context'],
            )
        except Exception:
            return JsonResponse(Msg().Error(), safe=False)
        return JsonResponse(Msg().Success(), safe=False)
