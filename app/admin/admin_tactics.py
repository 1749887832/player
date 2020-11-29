import json
import os
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
    def Data(self):
        # print(self.GET.get('page'))
        page = int(self.GET.get('page'))
        limit = int(self.GET.get('limit'))
        # print(self.GET.get('limit'))
        try:
            user = UserProfile.objects.get(user_id=self.user.id)
            team_id = user.team_id
            tactics = Tactics.objects.filter(team_id=team_id)[limit * (page - 1):page * limit]
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
            coach = UserProfile.objects.filter(team_id=team_id, rights=4)
            data = list()
            for i in coach:
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
            print(i)
            context = i[1:len(i)-1].strip(',').split(',')
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
