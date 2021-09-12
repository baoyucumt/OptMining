import pandas as pd
import random
import copy
from class_set import *

coal_list_a = []  # 综采队列表
coal_list_b = []  # 填充队列表
CROSS_RATE = 0.8
CROSS_COUNT = 3
COAL_14_16_MUTATION_RATE = 0.0005
COAL_15_MUTATION_RATE = 0.001
POP_SIZE = 40
N_GENERATIONS = 600



def get_type_coal_list():
    """
    :return:三种煤层的列表
    """
    global coal_list_a
    global coal_list_b

    data = pd.read_excel(r"PeiCai 的副本.xlsx")
    prev_data = pd.read_excel(r"十二矿煤层层位表.xlsx", 1)

    for index, row in data.iterrows():
        a = []
        for _, col in row.iteritems():
            a.append(col)
        coal = Coal(*a)    #读入整个煤层属性表，进入

        # 添加16-17煤层的先序煤
        if coal.coal_seam == '己16-17煤层':
            for d in prev_data['层3']:
                if coal.name == d:
                    result = prev_data[prev_data['层3'] == d]
                    coal.prev = list(result['层2'].values)
                    break
        # 添加15煤层的先序煤
        elif coal.coal_seam == '己15煤层':
            for d in prev_data['层2']:
                if coal.name == d:
                    result = prev_data[prev_data['层2'] == d]
                    coal.prev = list(result['层1'].values)
                    break
        if coal.mining_status == '未采' and coal.coal_seam == '己16-17煤层':
            coal_list_a.append(coal)
        elif coal.mining_status == '未采' and coal.coal_seam == '己14煤层':
            coal_list_a.append(coal)
        elif coal.mining_status == '未采' and coal.coal_seam == '己15煤层':
            if coal.name == 31020:
                coal_list_b = [coal] + coal_list_b
            else:
                coal_list_b.append(coal)


def add_index():
    """
    为15煤添加属性 prev_index:[]   表示15煤先序的下标
                  back_index:[]   表示15煤压着的16煤下标
    :return:
    """
    global coal_list_b
    global coal_list_a

    for i in coal_list_b:
        for index, j in enumerate(coal_list_a):
            if j.coal_seam == "己14煤层" and j.name in i.prev:
                i.prev_index.append(index)
    for index, m in enumerate(coal_list_a):
        if m.coal_seam == "己14煤层":
            continue
        for n in coal_list_b:
            if m.coal_seam == "己16-17煤层" and n.name in m.prev:
                n.back_index.append(index)


# 15煤的基因编码
def get_code_15():
    """
    返回的是[0,1,2,3,4,....]代表下标的列表
    :return:
    """
    global coal_list_b
    code_15 = list(range(1, len(coal_list_b)))

    # 给15煤打乱顺序
    random.shuffle(code_15)
    return [0] + code_15


def getDNA():
    """
    :return: 返回随机的一个样本
    """
    code_15 = get_code_15()
    code_1416 = []
    len_1416 = len(coal_list_a)
    for i in range(len_1416):
        code_1416.append(random.randint(0, 1))

    return [code_1416, code_15]


def decode_gorup(DNA):
    """
    :param DNA:
    :return: 返回解码后的group
    """
    # 不备份的话不同样本之间会干扰
    coal_list_a_backup = copy.deepcopy(coal_list_a)

    decode_coal_15_list = []
    decode_mining_team1_list = []
    decode_mining_team2_list = []

    for i in DNA[1]:
        coal_list_b[i].team = '填充1队'
        decode_coal_15_list.append(coal_list_b[i])
        # 15煤的先序(14煤)
        for j in coal_list_b[i].prev_index:
            tmp = coal_list_a_backup[j]
            if hasattr(tmp,"selected"):   # 已经被其他15煤层加入了
                continue
            if DNA[0][j] == 0:
                # 综采队1
                tmp.team = '综采1队'
                tmp.selected = 1
                decode_mining_team1_list.append(tmp)
            elif DNA[0][j] == 1:
                # 综采队2
                tmp.team = '综采2队'
                tmp.selected = 1
                decode_mining_team2_list.append(tmp)

    # 可能有不被15煤层依赖的14煤,加入到队伍的列表中
    for index,coal14 in enumerate(coal_list_a_backup):
        if coal14.coal_seam == "己14煤层" and not hasattr(coal14,"selected"):
            if DNA[0][index] == 0:
                coal14.team = '综采1队'
                coal14.selected = 1
                decode_mining_team2_list.append(coal14)
            elif DNA[0][index] == 1:
                coal14.team = '综采2队'
                coal14.selected = 1
                decode_mining_team2_list.append(coal14)

    # 记录两个队伍分配完14煤层之后的长度
    len_mining_team1 = len(decode_mining_team1_list)
    len_mining_team2 = len(decode_mining_team2_list)


    for i in decode_coal_15_list:
        # 15煤的后序(16煤)
        for k in i.back_index:
            tmp = coal_list_a_backup[k]
            if hasattr(tmp,"selected"):   # 已经被其他15煤层加入了
                continue
            if DNA[0][k] == 0:
                # 综采队1
                tmp.team = '综采1队'
                tmp.selected = 1
                decode_mining_team1_list.append(tmp)
            elif DNA[0][k] == 1:
                # 综采队2
                tmp.team = '综采2队'
                tmp.selected = 1
                decode_mining_team2_list.append(tmp)
    # 可能有完全不依赖15煤层的16煤层,加入到最前面,因为不需要等待
    for index, coal16 in enumerate(coal_list_a_backup):
        if coal16.coal_seam == "己16-17煤层" and not hasattr(coal16, "selected"):
            if DNA[0][index] == 0:
                coal16.team = '综采1队'
                coal16.selected = 1
                decode_mining_team1_list.insert(len_mining_team1,coal16)
            elif DNA[0][index] == 1:
                # 综采队2
                coal16.team = '综采2队'
                coal16.selected = 1
                decode_mining_team2_list.insert(len_mining_team2,coal16)
    group = get_group(decode_mining_team1_list,decode_coal_15_list,decode_mining_team2_list)
    return group


def get_group(decode_mining_team1_list,decode_coal_15_list,decode_mining_team2_list):
    team1 = Team('综采队', '综采1队', decode_mining_team1_list)
    team2 = Team('充填队', '填充1队', decode_coal_15_list)
    team3 = Team('综采队', '综采2队', decode_mining_team2_list)
    group = [team1, team2, team3]
    return group

def mutate(child_list):
    """
    :param child_list: 一个交叉后的DNA列表
    :return: 返回变异后的新分组
    """
    new_child_list = []
    for child in child_list:
        c = copy.deepcopy(child)
        # 对14/16煤进行变异
        for i in range(len(c[0])):
            if random.random() < COAL_14_16_MUTATION_RATE:
                c[0][i] = 1 if c[0][i] == 0 else 0
        # 对15煤进行变异
        len_coal_15 = len(c[1])
        for j in range(len_coal_15):
            if random.random() < COAL_15_MUTATION_RATE:
                change_index = random.randint(0,len_coal_15-1)
                c[1][j],c[1][change_index] = c[1][change_index],c[1][j]
        new_child_list.append(c)
    return new_child_list

def get_fitness(average_annual_output):
    """
    计算适应度
    :param average_annual_output: 平均年产量的列表
    :return: 返回每个样本计算后的适应度值
    """
    total = sum(average_annual_output)
    return [i/total for i in average_annual_output]

def select(current_groups,fitness):
    """
    选择样本,按照概率选择即可   random.choice
    :param current_groups:当前所有的样本分组 [group1,group2,....,groupn]
    :param fitness: 适应度
    :return: 返回选择后的新样本
    """
    return random.choices(current_groups, weights=fitness, k=POP_SIZE)

# 交叉
def get_couple(group_list):
    child_list = []
    for i in range(len(group_list)):
        mom_random = random.randint(0,len(group_list)-1)
        while mom_random == i:
            mom_random = random.randint(0,len(group_list)-1)
        child_list.append([cross_couple(group_list[i][0],group_list[mom_random][0]),group_list[i][1]])
    return child_list


# 产生子代
def cross_couple(dad, mom):
    cross_rate = random.random()
    child_a = []
    child_b = []
    if cross_rate < CROSS_RATE:
        cross_place = random.randint(0,len(dad)-1)
        child_a = dad[0:cross_place] + mom[cross_place:]
        child_b = mom[0:cross_place] + dad[cross_place:]
        choose = random.random()
        if choose < 0.5:
            return child_a
        else:
            return child_b
    else:
        return dad


def crossover(pop):
    for i in range(len(pop)):
        if random.random() < CROSS_RATE:
            mom_index = random.randint(0,len(pop)-1)
            while mom_index == i:
                mom_index = random.randint(0,len(pop)-1)
            for j in range(len(pop[i][0])):
                if random.randint(0, 1) == 1:
                    pop[i][0][j],pop[mom_index][0][j] = pop[mom_index][0][j],pop[i][0][j]
    return pop

if __name__ == "__main__":
    get_type_coal_list()
    add_index()
    print(coal_list_a)
    print(coal_list_b)
    a = getDNA()
    print(a)
    print(mutate([a,a,a]))
    # print(decode_gorup(a)[0].coal_seam_list)
    # print(decode_gorup(a)[2].coal_seam_list)
