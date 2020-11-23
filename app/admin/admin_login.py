from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.base import View


class Admin_log(View):
    def __init__(self):
        self.POST = None
        super().__init__()

    # 跳转到登录页面
    def super_login(self):
        return render(self, 'super_login.html')

    # 验证用户登录
    def TestUser(self):
        if self.POST:
            username = self.POST.get('username', None)
            password = self.POST.get('password', None)
            # user = User.objects.create_user(username=username,password=password)
            # profile = UserProfile()
            # profile.user_id = user.id
            # profile.save()
            # return render(request,'super_login.html')
            # 进行登录认证,
            user = authenticate(username=username, password=password)
            # 判断用户是否存在
            if user is not None:
                if user.is_superuser:
                    # 这里的登录, 表示的是将用户信息添加到session中
                    login(self, user)
                    return redirect('/player/system_min/')
                else:
                    return render(self, 'super_login.html', {"msg": "抱歉您没有这个权限"})
            else:
                return render(self, 'super_login.html', {"msg": "登录失败"})
        else:
            return render(self, 'super_login.html')


class Admin_LogOut(View):
    def __init__(self):
        self.POST = None
        super(Admin_LogOut, self).__init__()

    # 安全退出
    def LogOut(self):
        logout(self)
        return redirect('/player/slogin/')