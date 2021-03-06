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
import app.admin.admin_command as Com
import app.admin.admin_finance as Fina
import app.admin.admin_setting as Set
import app.admin.ceshi as ce

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
    # 解约球员
    path('player/del_player/', Show.ShowTeam.DelPlyaer),
    # 修改传参
    path('player/real_updateuser/', Show.ShowTeam.RalUpdatePlayer),
    # 上传头像接口
    path('player/update_pic/', Show.ShowTeam.Update_pic),
    # 我的球员信息数据回显
    path('player/select_myplayer/', Show.ShowTeam.Select_myplayer),
    # 战术管理接口
    path('player/tactics/', Ta.P_Tactics.Show_all),
    # 查询所有战术
    path('player/data/', Ta.P_Tactics.Data),
    # 新建战术页面跳转
    path('player/create_tactics/', Ta.P_Tactics.Create_tatics),
    # 教练接口
    path('player/select_coach/', Ta.P_Tactics.Select_coach),
    # 球员接口
    path('player/select_player/', Ta.P_Tactics.Select_player),
    # 图片接口
    path('player/pic/', Ta.P_Tactics.Create_pic),
    # 创建战术接口
    path('player/create_tactic/', Ta.P_Tactics.Create_tatic),
    # 删除战术接口
    path('player/del_tactic/', Ta.P_Tactics.Del_tatics),
    # 查看战术详情接口
    path('player/title_context/', Ta.P_Tactics.Title_context),
    # 编辑战术接口
    path('player/update_tatics/', Ta.P_Tactics.Update_tatics),
    # 编辑战术回显
    path('player/p_tatics/', Ta.P_Tactics.P_tatics),
    # 修改战术提交
    path('player/update_tatic/', Ta.P_Tactics.Update_tatic),
    # 查询战术标题接口
    # path('player/select_title/', Ta.P_Tactics.Select_title),
    # 数据中心接口
    path('player/record/', Re.Record.Show_all),

    # 数据中心球员板块
    path('player/record_player/', Re.Record.Record_show),
    # 查询赛季模块
    path('player/select_season/', Re.Record.Select_season),
    # 查询球员模块
    path('player/select_players/', Re.Record.Select_players),
    # 查询赛程模块
    path('player/player_schedule/', Re.Record.Select_schedule),
    # 添加球员数据
    path('player/add_playerdata/', Re.Record.Add_playerdata),
    # 显示球队数据
    path('player/show_teamrecord/', Re.Record.Show_teamrecord),
    # 球队数据对比
    path('player/team_contrast/', Re.Record.Team_contrast),
    # 查询所有球队
    path('player/select_team/', Re.Record.Select_team),

    # 打开球员命令中心
    path('player/command/', Com.Player_Command.Show_command),
    # 查询所有的命令
    path('player/show_command/', Com.Player_Command.Show_all),
    # 打开新建命令
    path('player/create_command/', Com.Player_Command.C_command),
    # 创建命令
    path('player/create_commands/', Com.Player_Command.Create_command),
    # 打开财务管理
    path('player/finance/', Fina.Finance.Show_finance),
    # 显示球队所有的工资
    path('player/showfinance/', Fina.Finance.Show_playerfinance),
    # 计算球队工资
    path('player/countmoney/', Fina.Finance.Count_money),
    # 打开设置中心
    path('player/setting/', Set.Setting.Show_setting),
    # 显示设置中心的薪资
    path('player/setting_money/', Set.Setting.Show_money),
    # 修改薪资设置
    path('player/update_setmoney/', Set.Setting.Update_money),
    # 显示设置中心的首发角色
    path('player/setting_roles/', Set.Setting.Show_roles),
    # 移除首发
    path('player/remvo_setrule/', Set.Setting.Del_roles),
    # 显示所有赛季
    path('player/setting_season/', Set.Setting.Show_season),
    # 设置当期赛季
    path('player/set_nowseaon/', Set.Setting.Set_nowseason),
    # 修改首发球员
    path('player/update_setplayers/', Set.Setting.Update_setplayers),
    # 测试接口
    path('ceshi/', ce.Ce.Ceshi)
]
