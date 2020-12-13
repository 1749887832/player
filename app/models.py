# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# 创建球队表
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    # 球队名称
    name = models.CharField(max_length=128, null=True)
    # 球标
    team_pic = models.CharField(max_length=128, default='images/default.png')
    # 建队时间
    date = models.DateTimeField(null=True)
    # 位置
    position = models.CharField(max_length=128, null=True)
    # 主教练
    head_cocah = models.CharField(max_length=128, null=True)
    # 球馆
    aarea = models.CharField(max_length=128, null=True)


# 创建用户表
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    # 连接user表
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    # 姓名
    name = models.CharField(max_length=128, null=True)
    # 性别
    sex = models.CharField(max_length=32, default='男')
    # 头像
    userpic = models.CharField(max_length=128, default='images/default.png')
    # 出生日期
    date = models.DateTimeField(null=True)
    # 年龄
    age = models.IntegerField(null=True)
    # 籍贯
    palace = models.CharField(max_length=128, null=True)
    # 权限
    rights = models.IntegerField(null=True)
    # 角色
    role = models.CharField(max_length=64, null=True)
    # 学校
    school = models.CharField(max_length=64, null=True)
    # 隶属球队
    team_id = models.IntegerField(null=True)


# 创建赛程表
class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    # 球队1
    team_one = models.IntegerField(null=False)
    # 球队2
    team_two = models.IntegerField(null=False)
    # 比赛时间
    time = models.DateTimeField(null=True)
    # 主场
    home = models.CharField(max_length=32, null=True)
    # 类型
    type = models.CharField(max_length=32, null=True)
    # 绑定赛季
    season_id = models.IntegerField(null=False)


# 创建球员基础信息表
class Player_Basic(models.Model):
    id = models.AutoField(primary_key=True)
    # 球员身份
    p_id = models.CharField(max_length=32, default='集训球员')
    # 球员状态
    state = models.CharField(max_length=32, default='健康')
    # 球衣号码
    number = models.IntegerField(null=True)
    # 球场位置
    position = models.CharField(max_length=32, null=True)
    # 录入状态
    enable = models.IntegerField(default=1)
    # 绑定user_id
    user_id = models.IntegerField(null=False)
    # 来源
    where_from = models.IntegerField(null=True)


# 创建集训表
class JiXun(models.Model):
    id = models.AutoField(primary_key=True)
    # 老板id
    boss_id = models.IntegerField(null=False)
    # 球员id
    player_id = models.IntegerField(null=False)


# 创建球员提测表
class Player_Data(models.Model):
    id = models.AutoField(primary_key=True)
    # 身高
    height = models.FloatField(null=True)
    # 体重
    weight = models.FloatField(null=True)
    # 体脂
    body_fat = models.FloatField(null=True)
    # 站立摸高
    s_reach = models.FloatField(null=True)
    # 臂展
    wingspan = models.FloatField(null=True)
    # 卧推
    b_press = models.FloatField(null=True)
    # 冲刺跑
    s_run = models.FloatField(null=True)
    # 折返跑
    b_run = models.FloatField(null=True)
    # 罚篮
    f_basket = models.FloatField(null=True)
    # 绑定球员id
    user_id = models.IntegerField(null=True)
    # 特长
    specialty = models.CharField(max_length=64, null=True)


#  创建合同类型表
class SignUp(models.Model):
    id = models.AutoField(primary_key=True)
    # 合同类型
    type = models.CharField(max_length=64, null=False)
    # 合同年限
    year = models.IntegerField(null=False)
    # 薪资
    money = models.IntegerField(null=False)
    # 交易否决权
    jiaoyi = models.CharField(max_length=32, null=False)
    # 球员选项
    p_chance = models.CharField(max_length=32, null=False)
    # 球员选项年
    p_year = models.IntegerField(null=True)
    # 签约时间
    create_time = models.DateTimeField(null=True)
    # 球员id
    user_id = models.IntegerField(null=False)


# 创建战术模块表
class Tactics(models.Model):
    id = models.AutoField(primary_key=True)
    # 战术名称
    title = models.CharField(max_length=32, null=False)
    # 发起者
    start_player = models.CharField(max_length=64, null=False)
    # 终结者
    end_player = models.CharField(max_length=64, null=False)
    # 主导者
    main_player = models.CharField(max_length=64, null=False)
    # 战术详情
    context = models.CharField(max_length=128, null=True)
    # 战术图片或视频
    file = models.CharField(max_length=64, null=True)
    # 创建时间
    create_time = models.DateTimeField(null=True)
    # 创建人
    create_user = models.CharField(max_length=32, null=False)
    # 修改人
    update_uer = models.CharField(max_length=32, null=False)
    # 球队id
    team_id = models.IntegerField(null=True)


# 创建赛季表
class Season(models.Model):
    id = models.AutoField(primary_key=True)
    # 赛季名称
    name = models.CharField(max_length=68, null=True)


# 创建球员数据表
class Player_season(models.Model):
    id = models.AutoField(primary_key=True)
    # 得分
    score = models.CharField(max_length=32, null=True)
    # 上场时间
    time = models.CharField(max_length=32, null=True)
    # 投篮
    shoot = models.CharField(max_length=32, null=True)
    # 命中投篮数
    hit_shoot = models.CharField(max_length=32, null=True)
    # 三分
    three_points = models.CharField(max_length=32, null=True)
    # 命中三分熟
    hit_points = models.CharField(max_length=32, null=True)
    # 罚球
    free_throw = models.CharField(max_length=32, null=True)
    # 命中罚球数
    hit_throw = models.CharField(max_length=32, null=True)
    # 总篮板数
    all_court = models.CharField(max_length=32, null=True)
    # 前场篮板
    front_court = models.CharField(max_length=32, null=True)
    # 后场篮板
    back_court = models.CharField(max_length=32, null=True)
    # 助攻
    assists = models.CharField(max_length=32, null=True)
    # 抢断
    snatch = models.CharField(max_length=32, null=True)
    # 盖帽
    block_shot = models.CharField(max_length=32, null=True)
    # 失误
    error = models.CharField(max_length=32, null=True)
    # 犯规
    break_rules = models.CharField(max_length=32, null=True)
    # 球员
    player_id = models.IntegerField(null=False)
    # 赛季id
    season_id = models.IntegerField(null=False)
    # 赛程id
    schedule_id = models.IntegerField(null=False)
    # 球队id
    team_id = models.IntegerField(null=False)
