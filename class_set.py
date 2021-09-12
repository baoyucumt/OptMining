''' @File :class_set.py
    @Author:baoyu,zhangyu
    @Date :2021/7/1 19:19
    @Desc : '''

class Coal(object):
    def __init__(self, noid, id_, name, mine_name, coal_seam, advancing_length,
                 length, mining_status, average_coal_thickness, coal_density, coal_capacity,
                 daily_feed, cutting_depth_of_Shearer, recovery_rate, caving_recovery_rate,
                 gangue_density, coal_mining, mining_area, wings, mining_height, level, time_require,
                 nature_of_working_face,
                 mining_days, branch, gangue_rate, coefficient_of_crushing_expansion, elevation,
                 type_of_working_face, filling_material,filling_type):

        self.no=noid
        self.id = id_   # 编号
        self.name = name    #名称
        self.mine_name = mine_name  #矿名
        self.coal_seam = coal_seam  #煤层
        self.advancing_length = advancing_length  #工作面推进长度
        self.length = length                      #工作面长度
        self.mining_status = mining_status  #开采状态
        self.average_coal_thickness = average_coal_thickness  #平均煤厚
        self.coal_density= coal_density  #煤的容重
        self.coal_capacity = coal_capacity   #可采储量
        self.daily_feed = daily_feed   #日进刀数
        self.cutting_depth_of_Shearer = cutting_depth_of_Shearer   #采煤机截深
        self.recovery_rate = recovery_rate   #回采率
        self.caving_recovery_rate = caving_recovery_rate   #放顶回采率
        self.gangue_density = gangue_density   #矸石容重
        self.coal_mining = coal_mining   #采煤工艺
        self.mining_area = mining_area   #所属采区
        self.wings = wings   #翼别
        self.mining_height = mining_height   #采高
        self.level = level   #水平
        self.movetime_require = time_require   #搬家所需时间
        self.nature_of_working_face = nature_of_working_face   #工作面性质
        self.mining_days = mining_days   #回采天数
        self.branch = branch   #分支
        self.gangue_rate = gangue_rate   #含矸率
        self.coefficient_of_crushing_expansion = coefficient_of_crushing_expansion   #碎胀系数
        self.elevation = elevation   #标高
        self.type_of_working_face = type_of_working_face   #工作面类型
        self.filling_material = filling_material   # 充填材料
        self.filling_type = filling_type  # 充填工艺
        self.prev = None   #
        self.prev_index = []   #
        self.back_index = []    #
        self.movetime_require_backup=self.movetime_require  #备份一下，原值要减

    def __repr__(self):
        return '<名称:{},煤层:{},先序:{}>'.format(self.name, self.coal_seam, self.prev)


class Team(object):
    def __init__(self, type_, team_name, coal_list):
        self.type = type_
        self.team_name = team_name
        self.coal_seam_list = coal_list
        self.eachyear_total = []  # 年产量
        self.workdaysperyear=[]
        self.dayspassedperyear=[]
        self.gangueperyear=[]

    def __repr__(self):
        return f"<队伍名:{self.team_name}>"

class PubData(object):
    def __init__(self):
        self.StdProcdutionPerY=1040000   #新巨龙6240000
        self.minRatio =0.9
        self.ExpGanguePerY=240000 #每年掘进增加的矸石量30万吨
        self.SCHEDULINGTIME = 15  # 规划时间，年
        self.GASExtractionTime=90  #抽取瓦斯的时间,搬家30天，否则对应120天
        self.WORKDAYS=330  #一年工作天数
        self.MultiProcess=False  #是否使用多进程
        self.MPtype=1   #1表示 多进程
        self.FitnessType=1   #=1表示使用最大化产量，=2表示使用年产量的均方差
        self.POPSIZE=100
        self.N_GENERATIONS = 3000  #迭代次数
        self.Method='NSGAII'  # or GA
