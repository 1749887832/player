from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from app.models import UserProfile


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

    def showAllrole(self):
        global age1, age2
        user = UserProfile.objects.get(user_id=self.user.id)
        team_id = user.team_id
        name = self.POST.get('name')
        age = self.POST.get('age')
        # state = self.POST.get('state')
        role = self.POST.get('role')
        sex = self.POST.get('sex')
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
        all = UserProfile.objects.filter(team_id=team_id, name__icontains=name, sex__icontains=sex,
                                         age__range=[age1, age2], role__icontains=role)
        # print(all)
        date = list()
        for i in all:
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
        return JsonResponse(date, safe=False)
