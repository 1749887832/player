"""player URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import app.admin.admin_index as Ind
import app.admin.admin_login as Log
import app.admin.admin_find as Fin
import app.admin.admin_addplayer as Add
import app.admin.admin_showall as Show
import app.admin.admin_record as Re
import app.admin.admin_tactics as Ta
urlpatterns = [
    path('admin/', admin.site.urls),
    # 经理登录页面
    path('player/slogin/', Log.Admin_log.super_login),
    # 后台管理首页
    path('player/system_min/', Ind.Index.sys_min),
    # 验证后台登录
    path('player/yzlogin/', Log.Admin_log.TestUser),
    # 安全退出
    path('player/logout/', Log.Admin_LogOut.LogOut),
    # 跳到增加球员页面
    path('player/fplayer/', Fin.Admin_Find.AutoFind),
    # 添加球员
    path('player/create_player/', Fin.Admin_Find.CreatePlayer),
    # 添加角色
    path('player/create_role/', Fin.Admin_Find.CreateRole),
    # 跳到招募球员页面
    path('player/add_player/', Add.Admin_Add.AutoAdd),
    # 显示所有的球员的接口
    path('player/saplayer/', Add.Admin_Add.ShowAll),
    # 显示集训球员的接口
    path('player/jxplayer/', Add.Admin_Add.ShowJxplayer),
    # 显示试训球员的接口
    path('player/sxplayer/', Add.Admin_Add.ShowSxplayer),
    # 添加球员到集训名单中
    path('player/add_to_jx/', Add.Admin_Add.AddToJx),
    # 移出集训名单
    path('player/remove_to_jx/', Add.Admin_Add.RemoveToJx),
    # 试训球员
    path('player/player_sx/', Add.Admin_Add.PlayerSx),
    # 签约球员
    path('player/player_qy/', Add.Admin_Add.PlayerQy),
    # 跳转到我的团队页面
    path('player/showall/', Show.ShowTeam.showAll),
    # 查询该队所有的人
    path('player/show_all/', Show.ShowTeam.showAllrole),
    # 查询该队的球员
    path('player/show_player/', Show.ShowTeam.showAllPlayer),
    # 战术管理接口
    path('player/tactics/',Ta.Tactics.Show_all),
    # 测试返回接口
    path('player/data/',Ta.Tactics.Data),
    # 球员数据接口
    path('player/record/', Re.Record.Show_all)
]
