''' @File :timestamp.py @Author:张宇 @Date :2020/9/6 17:03 @Desc : '''
from datetime import datetime
import datetime as dt
import math
from utils.get_time import get_time
import copy
from utils.GA_2 import *
import time


finish_coal_list = []
FillingRate = 0.3

#计算产量
def caculate_output(team,min_least_time):
    if not team.coal_seam_list:
        return 0
    coal = team.coal_seam_list[0]
    if coal.mining_status == '未采' and hasattr(coal, 'begin_time'):
        if coal.coal_seam != "己15煤层":
            t = (coal.length * coal.average_coal_thickness * coal.cutting_depth_of_Shearer * coal.recovery_rate * coal.coal_capacity * coal.daily_feed) * min_least_time
            return t
        else:
            fill_speed = getattr(coal,'last_fill_speed',0)
            t = (coal.length * coal.average_coal_thickness * coal.recovery_rate * coal.coal_capacity * fill_speed) * min_least_time
            return t
    return 0

#查找先序煤层
def search_prev(coal_list,name,type="己15煤层"):
    prev_list = []
    for coal in coal_list:
        if coal.name in name and coal.coal_seam == type:
            prev_list.append(coal)
    if prev_list:
        return prev_list

    return None

def get_least_time(coal,now_time):
    return math.ceil(coal.advancing_length/(coal.daily_feed*coal.cutting_depth_of_Shearer))-int((now_time - coal.begin_time).days)

#获取推进速度
def get_fill_speed(coal,total_daily_stone):
    # kc不确定 填充面充实率(暂时取0.3)
    speed = (total_daily_stone*coal.coefficient_of_crushing_expansion)/(coal.gangue_capacity*coal.length*coal.mining_height*FillingRate)
    return speed
#计算日产矸量
def calculate_stone(coal):
    #recovery_rate 是需要回采率还是放顶回采率?
    return ((coal.length*coal.average_coal_thickness*coal.cutting_depth_of_Shearer*coal.recovery_rate*coal.daily_feed*coal.coal_capacity)*coal.gangue_content)/(1-coal.gangue_content)


def Judge(c,last_least_time):

    return (getattr(c,'least_time',-1) == 0 and c.mining_status == '未采') or c.mining_status == '已采'
def calculate_time(g):
    """
    :param group: 分组
    :return: 返回完成煤层序列与年产量列表
    """
    """
        group中结构:
            [team1,team2,team3]
        team对象属性:
            type:说明是填充队还是综采队
            coal_seam_list:该队伍对应的煤层类型  <list类型>
            coal_type:煤层类型
    """
    group = copy.deepcopy(g)
    ##彻底完成的煤层列表(指搬家也完成)
    global finish_coal_list
    finish_coal_list = []
    year_total = []  #年产量
    total = 0
    date = 0

    start = datetime(2020,1,1)
    now_time = real_now_time = start
    #综采队
    mining_group = []
    #填充队
    filling_group = []
    for team in group:
        if team.type == '充填队':
            filling_group.append(team)
        else:
            mining_group.append(team)
    last_least_time = float('inf')
    i = 1

    while any([team.coal_seam_list for team in filling_group]) or any([team.coal_seam_list for team in mining_group]):
        i += 1
        min_least_time = float('inf')

        ck = -1

        #遍历综采队
        for index,mining_team in enumerate(mining_group):
            #如果队伍中还有煤层未采,取出第一个
            if mining_team.coal_seam_list:
                coal = mining_team.coal_seam_list[0]
                if not hasattr(coal,'start_time'):
                    coal.start_time = real_now_time
                    coal.real_start_time = real_now_time
            else:
                continue
            ## 完成搬家
            if hasattr(coal,'least_time') and coal.least_time == 0 and coal.mining_status == '已采':
                coal.finish = True
                coal.end_time = now_time
                coal.real_end_time = real_now_time
                finish_coal = mining_team.coal_seam_list.pop(0)
                finish_coal_list.append(finish_coal)
                if mining_team.coal_seam_list:
                    coal = mining_team.coal_seam_list[0]
                    if not hasattr(coal,'start_time'):
                        coal.real_start_time = real_now_time
                        coal.start_time = now_time
                else:
                    continue

            if coal.coal_seam == '己14煤层':
                if not hasattr(coal,'begin_time'):
                    coal.begin_time = now_time
                    coal.real_begin_time = real_now_time
                    coal.least_time = math.ceil(coal.advancing_length/(coal.daily_feed*coal.cutting_depth_of_Shearer))
                elif hasattr(coal,'begin_time') and coal.mining_status == '未采':
                    coal.least_time = get_least_time(coal,now_time)
                elif hasattr(coal,'begin_time') and coal.mining_status == '已采':
                    coal.least_time -= last_least_time 

            elif coal.coal_seam == '己16-17煤层':
                #无先序
                if not coal.prev:
                    if not hasattr(coal, 'begin_time'):
                        coal.begin_time = now_time
                        coal.real_begin_time = real_now_time
                        coal.least_time = math.ceil(coal.advancing_length / (coal.daily_feed * coal.cutting_depth_of_Shearer))
                    elif hasattr(coal,'begin_time') and coal.mining_status == '未采':
                        coal.least_time = get_least_time(coal,now_time)
                    elif hasattr(coal,'begin_time') and coal.mining_status == '已采':
                        coal.least_time -= last_least_time 
                #有先序
                else:
                    coal_15_list = []
                    for filling_team in filling_group:
                        #查找其先序的15煤
                        coal_15_list += filling_team.coal_seam_list
                    prev_coal = search_prev(coal_15_list+finish_coal_list,coal.prev)
                    if not prev_coal or all(list(map(Judge,prev_coal,[last_least_time]*len(prev_coal)))) :
                        if not hasattr(coal, 'begin_time'):
                            coal.begin_time = now_time
                            coal.real_begin_time = real_now_time
                            coal.least_time = math.ceil(coal.advancing_length / (coal.daily_feed * coal.cutting_depth_of_Shearer))
                        elif hasattr(coal,'begin_time') and coal.mining_status == '未采':
                            coal.least_time = get_least_time(coal,now_time)
                        elif hasattr(coal,'begin_time') and coal.mining_status == '已采':
                            coal.least_time -= last_least_time 


            ## 完成采矿,但未搬家
            if hasattr(coal,'least_time') and coal.least_time == 0 and coal.mining_status == '未采':
                coal.mining_status = '已采'
                #采矿完成时间
                coal.finish_time = now_time
                coal.real_finish_time = real_now_time
                coal.least_time = coal.time_require
            if hasattr(coal,'least_time'):
                if coal.least_time<min_least_time:
                    min_least_time = coal.least_time
                    tmp = coal

        #遍历填充队
        for index,mining_team in enumerate(filling_group): 
            if mining_team.coal_seam_list:
                coal = mining_team.coal_seam_list[0]
                if not hasattr(coal,'start_time'):
                    coal.start_time = now_time
                    coal.real_start_time = real_now_time
            else:
                continue

            if hasattr(coal,'least_time') and coal.least_time == 0 and coal.mining_status == '已采':
                coal.finish = True
                coal.end_time = now_time
                coal.real_end_time = real_now_time
                finish_coal = mining_team.coal_seam_list.pop(0)
                finish_coal_list.append(finish_coal)
                if mining_team.coal_seam_list:
                    coal = mining_team.coal_seam_list[0]
                    if not hasattr(coal, 'start_time'):
                        coal.start_time = now_time
                        coal.real_start_time = real_now_time
                else:
                    continue

            #已采,等待都不可以
            if not coal.prev:
                #总日产矸量
                total_daily_stone = 0
                for team in mining_group:
                    #取出每个列表中第一个煤层
                    tmp_coal = team.coal_seam_list[0]
                    if coal.mining_status=='未采' and hasattr(coal,'begin_time') and (tmp_coal.coal_seam == '己14煤层' or tmp_coal.coal_seam == '己16-17煤层'):
                        total_daily_stone += calculate_stone(tmp_coal)
                total_daily_stone += 6000/330

                fill_speed = get_fill_speed(coal,total_daily_stone)
                coal.fill_speed = fill_speed
                if not hasattr(coal,'begin_time'):
                    coal.begin_time = now_time
                    coal.real_begin_time = real_now_time
                    coal.least_advancing_length = coal.advancing_length
                    coal.least_time = math.ceil(coal.least_advancing_length/fill_speed)
                elif hasattr(coal,'begin_time') and coal.mining_status == '未采':
                    #计算剩余推进面长度
                    coal.least_advancing_length -= getattr(coal,'last_fill_speed',default=0)*last_least_time
                    coal.least_time = math.ceil(coal.least_advancing_length/fill_speed)
                elif hasattr(coal,'begin_time') and coal.mining_status == '已采':
                    coal.least_time -= last_least_time

                coal.last_fill_speed = fill_speed
            else:
                coal_14_list = []
                for mining_team in mining_group:
                    coal_14_list += mining_team.coal_seam_list
                prev_coal = search_prev(coal_14_list+finish_coal_list,coal.prev,type='己14煤层')

                if not prev_coal:   # 没有先序煤,即是原本已经开采完成的
                    # 总日产矸量
                    total_daily_stone = 0
                    for team in mining_group:
                        # 取出每个列表中第一个煤层
                        if len(team.coal_seam_list) > 0:
                            tmp_coal = team.coal_seam_list[0]
                            if coal.mining_status == '未采' and hasattr(coal, 'begin_time') and (
                                    tmp_coal.coal_seam == '己14煤层' or tmp_coal.coal_seam == '己16-17煤层'):
                                total_daily_stone += calculate_stone(tmp_coal)
                    total_daily_stone += 6000 / 330
                    fill_speed = get_fill_speed(coal, total_daily_stone)
                    coal.fill_speed = fill_speed
                    if not hasattr(coal, 'begin_time'):
                        coal.begin_time = now_time
                        coal.real_begin_time = real_now_time
                        coal.least_advancing_length = coal.advancing_length
                        coal.least_time = math.ceil(coal.least_advancing_length / fill_speed)
                    elif hasattr(coal, 'begin_time') and coal.mining_status == '未采':
                        # 计算剩余推进面长度
                        coal.least_advancing_length -= getattr(coal, 'last_fill_speed', 0) * last_least_time
                        coal.least_time = math.ceil(coal.least_advancing_length / fill_speed)
                    elif hasattr(coal, 'begin_time') and coal.mining_status == '已采':
                        coal.least_time -= last_least_time

                    coal.last_fill_speed = fill_speed

                elif prev_coal and all(list(map(lambda x:x.mining_status == '已采',prev_coal))):
                    #先序煤的中距离最近完成天数
                    min_time = min([(now_time-i.finish_time).days for i in prev_coal])
                    if min_time >= 120:
                        
                        #总日产矸量
                        total_daily_stone = 0
                        for team in mining_group:
                            if len(team.coal_seam_list) > 0:
                                #取出每个列表中第一个煤层
                                tmp_coal = team.coal_seam_list[0]
                                if tmp_coal.mining_status=='未采' and hasattr(tmp_coal,'begin_time') and (tmp_coal.coal_seam == '己14煤层' or tmp_coal.coal_seam == '己16-17煤层'):
                                    total_daily_stone += calculate_stone(tmp_coal)
                        total_daily_stone += 6000/330
                        fill_speed = get_fill_speed(coal, total_daily_stone)

                        if not hasattr(coal,'begin_time'):
                            coal.begin_time = now_time
                            coal.real_begin_time = real_now_time
                            coal.least_advancing_length = coal.advancing_length
                            coal.least_time = math.ceil(coal.least_advancing_length/fill_speed)
                        elif hasattr(coal,'begin_time') and coal.mining_status == '未采':
                            #计算剩余推进面长度
                            coal.least_advancing_length -= getattr(coal,'last_fill_speed',0)*last_least_time
                            coal.least_time = math.ceil(coal.least_advancing_length/fill_speed)
                        elif hasattr(coal,'begin_time') and coal.mining_status == '已采':
                            coal.least_time -= last_least_time

                        coal.last_fill_speed = fill_speed
                    else:
                        coal.least_time = 120 - min_time


            ## 完成采矿,但未搬家,与其他两个矿不同,15煤需要判断剩余推进长度
            if hasattr(coal,'least_time') and getattr(coal,'least_advancing_length',1) <= 0 and coal.mining_status == '未采':
                coal.mining_status = '已采'
                coal.finish_time = now_time
                coal.real_finish_time = real_now_time
                coal.least_time = coal.time_require

            if hasattr(coal,'least_time'):

                if coal.least_time<min_least_time:
                    min_least_time = coal.least_time
                    tmp = coal
        if min_least_time == float('inf'):
            # 最后一次
            min_least_time = 0

        date += min_least_time
        # 小于一年
        if date <=  330:
            for team in mining_group:
                total += caculate_output(team, min_least_time)
            for team in filling_group:
                total += caculate_output(team, min_least_time)
        # 超过一年
        else:
            before_time = min_least_time - (date-330)
            after_time = date-330
            #前一年的
            for team in mining_group:
                total += caculate_output(team, before_time)
            for team in filling_group:
                total += caculate_output(team, before_time)

            year_total.append(total)
            total = 0
            date = 0
            if after_time > 330:
                while True:
                    total = 0
                    if after_time <= 330:
                        break
                    for team in mining_group:
                        total += caculate_output(team, 330)
                    for team in filling_group:
                        total += caculate_output(team, 330)
                    year_total.append(total)
                    after_time -= 330
            date += after_time
            for team in mining_group:
                total += caculate_output(team, after_time)
            for team in filling_group:
                total += caculate_output(team, after_time)
        #上一次最少天数
        last_least_time = min_least_time
        now_time += dt.timedelta(days=min_least_time)
        # 增加最少的天数
        real_now_time = get_time(real_now_time,min_least_time)
    # print(len(year_total))
    print(year_total)
    return sum(year_total)/len(year_total), finish_coal_list, year_total

if __name__ == '__main__':
    # group = get_group()
    # get_type_coal_list()
    # group = get_random_group()
    # max_coal_list = []
    # max_n = 0
    start = time.time()
    # while True:
    #     group = get_random_group()
    #     year_total = calculate_time(group)
    #     if len(finish_coal_list) > 41:
    #         max_coal_list = finish_coal_list
    #         max_n = len(finish_coal_list)
    #         break
    a = getDNA()
    group = decode_gorup(a)
    year_total = calculate_time(group)
    end = time.time()
    print("time:", end-start, "s")
    print(len(finish_coal_list),year_total,finish_coal_list)