import os
import uuid

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.admin.return_msg import Msg
from app.models import UserProfile, Player_Basic, Player_Data, SignUp


class ShowTeam:
    def __init__(self):
        self.FILES = None
        self.user = None
        self.POST = None
        super().__init__()

    def showAll(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_showall.html', context)

    @csrf_exempt
    def showAllrole(self):
        global age1, age2
        user = UserProfile.objects.get(user_id=self.user.id)
        team_id = user.team_id
        page = int(self.POST.get('page'))
        limit = int(self.POST.get('limit'))
        name = self.POST.get('name')
        age = self.POST.get('age')
        # state = self.POST.get('state')
        role = self.POST.get('role')
        sex = self.POST.get('sex')
        # print(role, name, age, sex)
        if age == '':
            age1 = 0
            age2 = 100
        elif age == '1':
            age1 = 0
            age2 = 20
        elif age == '2':
            age1 = 20
            age2 = 30
        elif age == '3':
            age1 = 30
            age2 = 100
        data = UserProfile.objects.filter(team_id=team_id, name__icontains=name, sex__icontains=sex,
                                          age__range=[age1, age2], role__icontains=role)
        all_date = data[limit * (page - 1):page * limit]
        count = len(data)
        # print(all)
        date = list()
        for i in all_date:
            context = dict()
            context['userid'] = i.id
            context['userpic'] = i.userpic
            context['name'] = i.name
            context['age'] = i.age
            context['role'] = i.role
            context['sex'] = i.sex
            context['palace'] = i.palace
            context['school'] = i.school
            date.append(context)
        # print(date)
        return JsonResponse(Msg().Success(date=date, count=count), safe=False)

    @csrf_exempt
    def showAllPlayer(self):
        global age1, age2
        user = UserProfile.objects.get(user_id=self.user.id)
        page = int(self.POST.get('page'))
        limit = int(self.POST.get('limit'))
        team_id = user.team_id
        name = self.POST.get('p_name')
        age = self.POST.get('p_age')
        state = self.POST.get('p_state')
        position = self.POST.get('p_position')
        sex = self.POST.get('p_sex')
        # print(role, name, age, sex)
        if age == '':
            age1 = '0'
            age2 = 100
        elif age == '1':
            age1 = 0
            age2 = 20
        elif age == '2':
            age1 = 20
            age2 = 30
        elif age == '3':
            age1 = 30
            age2 = 100
        try:
            player = UserProfile.objects.filter(team_id=team_id, name__icontains=name, sex__icontains=sex,
                                                age__range=[age1, age2], role="球员")
            basic = Player_Basic.objects.filter(state__icontains=state, position__icontains=position)
            count = 0
            date = list()
            for i in player:
                for j in basic:
                    if i.id == j.user_id:
                        context = dict()
                        context['userid'] = i.id
                        context['name'] = i.name
                        context['userpic'] = i.userpic
                        context['sex'] = i.sex
                        context['age'] = i.age
                        context['position'] = j.position
                        context['state'] = j.state
                        context['palace'] = i.palace
                        context['school'] = i.school
                        context['specialty'] = Player_Data.objects.get(user_id=j.id).specialty
                        count = count + 1
                        this_is_ceshi = count
                        if page * limit >= count:
                            date.append(context)
                        else:
                            pass
            # print(date)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
        return JsonResponse(Msg().Success(date=date, count=count), safe=False)

    def DelPlyaer(self):
        userid = self.POST.get('userid')
        try:
            is_not = SignUp.objects.get(user_id=UserProfile.objects.get(id=userid).user_id).jiaoyi
            if is_not == 'true':
                return JsonResponse(Msg().Success(msg='该球员有交易否决权，不可解约'))
            else:
                UserProfile.objects.filter(id=userid).update(
                    team_id=0
                )
                return JsonResponse(Msg().Success(msg='解约成功'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    @csrf_exempt
    def Update_pic(self):
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

    def Select_myplayer(self):
        userid = self.POST.get('userid')
        date = list()
        try:
            all_msg = UserProfile.objects.filter(id=userid)
            context = dict()
            for i in all_msg:
                context['user_id'] = i.user_id
                context['user_pic'] = i.userpic
                context['name'] = i.name
                context['sex'] = i.sex
                context['phone'] = User.objects.get(id=i.user_id).username
                context['data'] = i.date.strftime('%Y-%m-%d')
                date.append(context)
            return JsonResponse(Msg().Success(date=date), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    def RalUpdatePlayer(self):
        global picurl
        phone = self.POST.get('phone')
        try:
            if phone in [x.username for x in User.objects.all()]:
                return JsonResponse(Msg().Success(msg='手机号已经被注册'), safe=False)
            else:
                User.objects.filter(id=UserProfile.objects.get(id=self.POST.get('userid')).user_id).update(
                    username=self.POST.get('phone')
                )
                UserProfile.objects.filter(id=self.POST.get('userid')).update(
                    name=self.POST.get('username'),
                    sex=self.POST.get('sex'),
                    userpic=picurl,
                    date=self.POST.get('time'),
                    palace=self.POST.get('area'),
                    school=self.POST.get('school'),
                )
                return JsonResponse(Msg().Success(), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
