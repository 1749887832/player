from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
import datetime

from app.admin.return_msg import Msg
from app.models import UserProfile, Player_Basic, Player_Data, SignUp


class Admin_Add(View):
    def __init__(self):
        super().__init__()
        self.POST = None
        self.user = None

    def AutoAdd(self):
        user = UserProfile.objects.get(user_id=self.user.id)
        context = dict()
        context['date'] = user
        return render(self, 'system_recruit.html', context)

    # 显示所有的球员
    def ShowAll(self):
        try:
            team_id = UserProfile.objects.get(user_id=self.user.id).team_id
            global age1, age2
            page = int(self.POST.get('page'))
            limit = int(self.POST.get('limit'))
            name = self.POST.get('name')
            age = self.POST.get('age')
            state = self.POST.get('state')
            where = self.POST.get('where')
            sex = self.POST.get('sex')
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
            player = UserProfile.objects.filter(team_id=None, name__icontains=name, sex__icontains=sex,
                                                age__range=[age1, age2])
            basic = Player_Basic.objects.filter(
                where_from__in=[x.user_id for x in UserProfile.objects.filter(team_id=team_id)],
                state__icontains=state, position__icontains=where)
            date = list()
            count = 0
            for i in player:
                for j in basic:
                    if i.id == j.user_id:
                        context = dict()
                        context['userid'] = j.user_id
                        context["userpic"] = i.userpic
                        context["name"] = i.name
                        context["sex"] = i.sex
                        context["age"] = i.age
                        context["state"] = j.state
                        context["position"] = j.position
                        context["palace"] = i.palace
                        context["school"] = i.school
                        context['where_from'] = UserProfile.objects.get(user_id=j.where_from).name
                        count = count + 1
                        if count <= page * limit:
                            date.append(context)
                        else:
                            pass
            return JsonResponse(Msg().Success(date=date, count=count), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    # 显示集训名单的球员
    def ShowJxplayer(self):
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        try:
            global age1, age2
            page = int(self.POST.get('page'))
            limit = int(self.POST.get('limit'))
            name = self.POST.get('name')
            age = self.POST.get('age')
            state = self.POST.get('state')
            where = self.POST.get('where')
            sex = self.POST.get('sex')
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
            player = UserProfile.objects.filter(team_id=None, name__icontains=name, sex__icontains=sex,
                                                age__range=[age1, age2])
            basic = Player_Basic.objects.filter(
                where_from__in=[x.user_id for x in UserProfile.objects.filter(team_id=team_id)],
                state__icontains=state, position__icontains=where, enable=2)
            count = 0
            date = list()
            for j in basic:
                for k in player:
                    if j.user_id == k.id:
                        context = dict()
                        context['userid'] = j.id
                        context["userpic"] = k.userpic
                        context["name"] = k.name
                        context["sex"] = k.sex
                        context["age"] = k.age
                        context["state"] = j.state
                        context["position"] = j.position
                        context["palace"] = k.palace
                        context["school"] = k.school
                        context['where_from'] = UserProfile.objects.get(user_id=j.where_from).name
                        count = count + 1
                        if page * limit >= count:
                            date.append(context)
                        else:
                            pass
                    pass
                pass
            return JsonResponse(Msg().Success(date=date, count=count), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    # 显示试训的球员
    def ShowSxplayer(self):
        team_id = UserProfile.objects.get(user_id=self.user.id).team_id
        try:
            global age1, age2
            name = self.POST.get('name')
            age = self.POST.get('age')
            state = self.POST.get('state')
            where = self.POST.get('where')
            sex = self.POST.get('sex')
            page = int(self.POST.get('page'))
            limit = int(self.POST.get('limit'))
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
            player = UserProfile.objects.filter(team_id=None, name__icontains=name, sex__icontains=sex,
                                                age__range=[age1, age2])
            basic = Player_Basic.objects.filter(
                where_from__in=[x.user_id for x in UserProfile.objects.filter(team_id=team_id)],
                state__icontains=state, position__icontains=where, enable=3)
            player_data = Player_Data.objects.all()
            date = list()
            count = 0
            for i in player_data:
                for j in basic:
                    for k in player:
                        if j.user_id == k.id and i.user_id == j.id:
                            context = dict()
                            context['userid'] = k.user_id
                            context["userpic"] = k.userpic
                            context["name"] = k.name
                            context["sex"] = k.sex
                            context["age"] = k.age
                            context["state"] = j.state
                            context["position"] = j.position
                            context["palace"] = k.palace
                            context["school"] = k.school
                            context['height'] = i.height
                            context['weight'] = i.weight
                            context['body_fat'] = i.body_fat
                            context['s_reach'] = i.s_reach
                            context['wingspan'] = i.wingspan
                            context['b_press'] = i.b_press
                            context['s_run'] = i.s_run
                            context['b_run'] = i.b_run
                            context['f_basket'] = i.f_basket
                            context['where_from'] = UserProfile.objects.get(user_id=j.where_from).name
                            count = count + 1
                            if page * limit >= count:
                                date.append(context)
                            else:
                                pass
            return JsonResponse(Msg().Success(date=date, count=count), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    # 加入集训名单
    def AddToJx(self):
        try:
            userid = self.POST.get('userid')
            user = Player_Basic.objects.filter(enable=1, user_id=userid)
            if len(user) > 0:
                Player_Basic.objects.filter(user_id=userid).update(enable=2)
                return JsonResponse(Msg().Success(msg='加入集训成功'), safe=False)
            else:
                return JsonResponse(Msg().Success(msg='该球员已在集训名单中'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    # 移出集训名单
    def RemoveToJx(self):
        try:
            userid = self.POST.get('userid')
            Player_Basic.objects.filter(id=userid).update(enable=1)
            return JsonResponse(Msg().Success(msg='移除集训名单成功'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    # 试训球员
    def PlayerSx(self):
        try:
            userid = self.POST.get('userid')
            height = self.POST.get('height')
            weight = self.POST.get('weight')
            body_fat = self.POST.get('body_fat')
            s_reach = self.POST.get('s_reach')
            wingspan = self.POST.get('wingspan')
            b_press = self.POST.get('b_press')
            s_run = self.POST.get('s_run')
            b_run = self.POST.get('b_run')
            f_basket = self.POST.get('f_basket')
            specialty = self.POST.get('specialty')
            player_data = Player_Data.objects.create(
                user_id=userid,
                height=height,
                weight=weight,
                body_fat=body_fat,
                s_reach=s_reach,
                wingspan=wingspan,
                b_press=b_press,
                s_run=s_run,
                b_run=b_run,
                f_basket=f_basket,
                specialty=specialty,
            )
            player_data.save()
            Player_Basic.objects.filter(id=userid).update(enable=3)
            return JsonResponse(Msg().Success(msg='试训成功'), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)

    def PlayerQy(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(time)
        if self.POST.get('p_chance') == 'true':
            p_year = self.POST.get('p_year')
        else:
            p_year = 0
        try:
            signup = SignUp.objects.create(
                user_id=self.POST.get('user_id'),
                type=self.POST.get('type'),
                year=self.POST.get('year'),
                money=self.POST.get('money'),
                jiaoyi=self.POST.get('jiaoyi'),
                p_chance=self.POST.get('p_chance'),
                p_year=p_year,
                create_time=time
            )
            signup.save()
            UserProfile.objects.filter(user_id=self.POST.get('user_id')).update(
                team_id=UserProfile.objects.filter(user_id=self.user.id)[0].team_id)
            Player_Basic.objects.filter(
                user_id=UserProfile.objects.filter(user_id=self.POST.get('user_id'))[0].id).update(enable=0)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
        return JsonResponse(Msg().Success(msg='签约成功'), safe=False)
