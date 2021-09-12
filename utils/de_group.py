''' @File :de_group.py @Author:张宇 @Date :2021/2/7 12:18 @Desc : '''

"""
对finish_coal_list进行分解，分别放入对应的队伍中
"""

def de_group(finish_coal_list):
    """

    :param finish_coal_list: 完成的顺序列表
    :return: 三个队伍开采煤的序列
    """
    coal_15_list = []
    mining_team1_list = []
    mining_team2_list = []
    for coal in finish_coal_list:
        if not hasattr(coal,"team"):
            print(coal)
        if coal.team == '综采1队':
            mining_team1_list.append(coal)
        elif coal.team == '综采2队':
            mining_team2_list.append(coal)
        else:
            coal_15_list.append(coal)


    return coal_15_list,mining_team1_list,mining_team2_list