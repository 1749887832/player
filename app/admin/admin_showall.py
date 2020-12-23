from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from app.admin.return_msg import Msg
from app.models import UserProfile, Player_Basic, Player_Data


class ShowTeam:
    def __init__(self):
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
        data = UserProfile.objects.filter(team_id=team_id, name__icontains=name, sex__icontains=sex, age__range=[age1, age2], role__icontains=role)
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
                        count = count + 1
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
                        date.append(context)
            # print(date)
        except Exception as e:
            print(e)
            return JsonResponse(Msg().Error(), safe=False)
        return JsonResponse(Msg().Success(date=date, count=count), safe=False)
