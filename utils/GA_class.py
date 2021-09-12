''' @File :class_set.py
    @Author:baoyu
    @Date :2021/7/1 19:19
    @Desc : '''
import pandas as pd
import random
import copy
import  numpy as np
from class_set import *

global coal_list_a
global coal_list_b
global coal_list_c

class GA_C:
    def __init__(self):
        pud=PubData()
        global coal_list_a
        coal_list_a= []  # 综采队列表
        global coal_list_c
        coal_list_c = []  # 综采队列表
        global coal_list_b
        coal_list_b= []  # 填充队列表
        self.CROSS_RATE = 0.8
        self.CROSS_COUNT = 3
        self.COAL_14_16_MUTATION_RATE = 0.5
        self.COAL_15_MUTATION_RATE = 0.5
        self.FILLRATE_MUTATION_RATE = 0.5
        self.POP_SIZE = pud.POPSIZE #40
        self.NEWPOP_PERTIME=0.3  #每次选择后，重新生成的替换比例
        self.N_GENERATIONS = pud.N_GENERATIONS
        self.fillTeamNum=2  #充填队数目
        self.ExpTeamNum = 2  #综采对数目
        self.SelectedProb=0.4  #选择去除的概率
        self.SaveGoodRate=0.1
        self.GASExtractionTime=pud.GASExtractionTime
        self.fillratevalue=0.5
        self.FitnessType=pud.FitnessType  #使用目标函数的类型，产量或均方差
        self.get_type_coal_list() # 初始化数据读入
        self.add_index()  #添加充填层15层前后序的索引


    def get_type_coal_list(self):
        """
        :return:三种煤层的列表
        """
        global coal_list_a
        global coal_list_b
        global coal_list_c

        data = pd.read_excel(r"PeiCai.xlsx")  #data = pd.read_excel(r"PeiCai 的副本.xlsx")
        prev_data = pd.read_excel(r"十二矿煤层层位表.xlsx", 1)

        for index, row in data.iterrows():
            a = []
            for _, col in row.iteritems():
                a.append(col)
            coal = Coal(*a)  #取coal数据

            # 添加16-17煤层的先序煤
            if coal.coal_seam == '己16-17煤层':
                for d in prev_data['层3']:
                    if not np.isnan(d) and str(coal.name) == str(int(d)):    #字符串
                        result = (prev_data[prev_data['层3'] == d])
                        coal.prev = list(result['层2'].values)
                        break
            # 添加15煤层的先序煤
            elif coal.coal_seam == '己15煤层':
                for d in prev_data['层2']:
                    if str(coal.name) == str(int(d)):
                        result = (prev_data[prev_data['层2'] == d])
                        coal.prev = list(result['层1'].values)
                        break
            if coal.mining_status == '未采' and coal.coal_seam == '己16-17煤层':
                coal_list_c.append(coal)
            elif coal.mining_status == '未采' and coal.coal_seam == '己14煤层':
                coal_list_a.append(coal)
            elif coal.mining_status == '未采' and coal.coal_seam == '己15煤层':
                if coal.name == 31020:  #???
                    coal_list_b = [coal] + coal_list_b
                else:
                    coal_list_b.append(coal)
        self.InsertGasTime(coal_list_b,coal_list_a)
        coal_list_a.extend(coal_list_c)

    # 对抽采层进行处理
    def InsertGasTime(self, coal_list, upcoal_list):
        prev_list = []
        for coal in coal_list:  # 是不是一个字符一个数值？
            for coal2 in upcoal_list:
                if str(coal2.name) in coal.prev or (coal2.name) in coal.prev :
                    if coal2.mining_status == '未采':
                        if not hasattr(coal, 'gaswaitdays'):  # 有先序，且未开采,gas添加
                            coal.gaswaitdays = self.GASExtractionTime

    def add_index(self):
        """
        为15煤添加属性 prev_index:[]   表示15煤先序的下标
                      back_index:[]   表示15煤压着的16煤下标
        :return:
        """
        global coal_list_b
        global coal_list_a
        global coal_list_c

        for i in coal_list_b:
            for index, j in enumerate(coal_list_a):
                if i.prev and j.coal_seam == "己14煤层" and j.name in i.prev:
                    i.prev_index.append(index)
        for index, m in enumerate(coal_list_a):
            if m.coal_seam == "己14煤层":
                continue
            for n in coal_list_b:
                if m.prev and m.coal_seam == "己16-17煤层" and n.name in m.prev:
                    n.back_index.append(index)


    # 15煤的基因编码
    def get_code_15(self):
        """
        返回的是[0,1,2,3,4,....]代表下标的列表
        :return:
        """
        global coal_list_b
        code_15=[]
        #code_15 = list(range(1, len(coal_list_b)))
        for index in enumerate(coal_list_b):
            code_15.append(index[1].name)
        # 给15煤打乱顺序
        random.shuffle(code_15)  #随机排序
        return code_15   #0?     原来有[0] +


    def getDNA(self):
        """
        :return: 返回随机的一个样本
        """
        code_15 = self.get_code_15()
        code_1416 = []
        len_1416 = len(coal_list_a)
        #for i in range(len_1416):
        #    code_1416.append(random.randint(0, 1))
        for index in enumerate(coal_list_a):
            code_1416.append(index[1].name)
        random.shuffle(code_1416)  # 随机排序
        self.CreateFillRate()  # 随机充实率
        return [code_1416, code_15, self.fillratevalue]


    def CreateFillRate(self):
        self.fillratevalue = random.randint(30,95)/100  # 随机充实率
        return self.fillratevalue

    def decode_gorup(self,name, DNA):
        """
        :param DNA:
        :return: 返回解码后的group
        """
        # 不备份的话不同样本之间会干扰
        coal_list_a_backup = copy.deepcopy(coal_list_a)
        if(len(name)>2):
            DNA=DNA[0]
        decode_coal_15_list = []
        decode_mining_team1_list = []
        decode_mining_team2_list = []
        #facecount=0
        for i in range(len(DNA[1])):
            #if facecount % 2==0:
            coal_list_b[i].team = 0  #充填队的编号设定为0和1，相当于只有一个充填队不间断工作
            #else:
            #    coal_list_b[i].team=1
            #facecount=facecount+1

            decode_coal_15_list.append(DNA[1][i])
        '''
        facecount = 0
        for j in range(len(DNA[0])):  #分别加入两个综采序列，使用内部交叉法
            if facecount % 2 == 0:
                decode_mining_team1_list.append(DNA[0][j])
            else:
                decode_mining_team2_list.append(DNA[0][j])
            facecount = facecount + 1
        '''
        mid=int(len(DNA[0])/2)
        decode_mining_team1_list=DNA[0][0:mid]
        decode_mining_team2_list = DNA[0][mid:]
        group = self.get_group(decode_mining_team1_list,decode_coal_15_list,decode_mining_team2_list)
        return [group,DNA[2]]


    def get_group(self, decode_mining_team1_list,decode_coal_15_list,decode_mining_team2_list):
        decode_mining_team1_list_tmp=[]
        decode_mining_team2_list_tmp=[]
        decode_coal_15_list_tmp=[]
        for i in range(len(decode_mining_team1_list)):  #充填队转码
            for j in coal_list_a:
                if j.name==decode_mining_team1_list[i]:
                    tmp=copy.deepcopy(j)
                    decode_mining_team1_list_tmp.append(tmp)
                    break
        for i in range(len(decode_mining_team2_list)):  #充填队转码
            for j in coal_list_a:
                if j.name==decode_mining_team2_list[i]:
                    tmp = copy.deepcopy(j)
                    decode_mining_team2_list_tmp.append(tmp)
                    break
        for i in range(len(decode_coal_15_list)):  #充填队转码
            for j in coal_list_b:
                if j.name==decode_coal_15_list[i]:
                    tmp = copy.deepcopy(j)
                    decode_coal_15_list_tmp.append(tmp)
                    break
        team1 = Team('综采队', '综采1队', decode_mining_team1_list_tmp)
        team2 = Team('充填队', '填充1队', decode_coal_15_list_tmp)
        team3 = Team('综采队', '综采2队', decode_mining_team2_list_tmp)
        group = [team1, team2, team3]
        return group

    def mutate(self, child_list):# 变异，就是随机挑两个互换，15要单独变异,最好的应该保持
        """
        :param child_list: 一个交叉后的DNA列表
        :return: 返回变异后的新分组
        """
        new_child_list = []
        savecount=int(len(child_list)*self.SaveGoodRate)  #保留最好的
        for child in child_list[savecount:]:
            c = copy.deepcopy(child)
            # 对14/16煤进行变异
            #for i in range(len(c[0])):
            if random.random() < self.COAL_14_16_MUTATION_RATE:
                loc1=random.randint(0,len(c[0])-1)
                loc2 = random.randint(0, len(c[0])- 1)
                c[0][loc1], c[0][loc2] = c[0][loc2], c[0][loc1]
            # 对15煤进行变异
            #len_coal_15 = len(c[1])
            #for j in range(len_coal_15):
            if random.random() < self.COAL_15_MUTATION_RATE:
                loc1 = random.randint(0, len(c[1]) - 1)
                loc2 = random.randint(0, len(c[1]) - 1)
                c[1][loc1],c[1][loc2] = c[1][loc2],c[1][loc1]
            if random.random() < self.FILLRATE_MUTATION_RATE:  #充实率
                c[2]= self.CreateFillRate() # 随机充实率
                #if c[2]==0:
                #    c[2]=0.1
            new_child_list.append(c)
        return child_list[:savecount]+new_child_list

    def get_fitness(self,average_annual_output,type):
        """
        计算适应度
        :param average_annual_output: 平均年产量的列表
        :return: 返回每个样本计算后的适应度值
        """
        if type==0: #单进程产量
            tmp = [(average_annual_output[i][0]) for i in range(len(average_annual_output))]
            total = sum(tmp)
        elif type==1:  #使用多进程
            tmp=[(average_annual_output[i][0]) for i in range(len(average_annual_output))]
            total = sum(tmp)
        elif type==2: #单进程方差
            tmp=[(average_annual_output[i][2]) for i in range(len(average_annual_output))]

        #if total==0:
        #    return [0.1 for i in tmp]
        #return [i/total for i in tmp]
        return tmp

    def mykeycmp(self,elem):
        return elem[1]
    def select(self,current_groups,fitness):
        """
        选择样本,按照概率选择即可   random.choice
        :param current_groups:当前所有的样本分组 [group1,group2,....,groupn]
        :param fitness: 适应度
        :return: 返回选择后的新样本
        """
        tmp=sorted(zip(fitness,current_groups),reverse=True)  #两个list关联排序,只能一次，奇怪
        if self.FitnessType==2:
            tmp = sorted(zip(fitness, current_groups))
        fitness,current_groups=zip(*tmp)
        #total=sum(fitness)
        #prob=np.array(fitness)/total  #[a/b for a,b in zip(fitness,total)
        fitness=list(fitness)
        countfit=len(fitness)
        current_groups=list(current_groups)
        i=0
        while countfit>0:  #去重，可以使用集合，但处理两个没有试验
            for j in range(countfit-1,1,-1):
                if i>j:
                    break
                if fitness[i] == fitness[j]:
                    fitness.pop(j)
                    current_groups.pop(j)
                    countfit-=1
            i+=1
            if i>=countfit:
                break
        delno = np.floor(self.POP_SIZE * self.SelectedProb)
        #if delno>self.POP_SIZE-len(fitness):  #删除了，还要补上
        delno-=self.POP_SIZE-len(fitness)
        cutpop=0
        while cutpop<delno : #删除最差的
            tmpval=np.argmin(fitness)
            if self.FitnessType==2:
                tmpval=np.argmax(fitness)
            fitness.pop(tmpval)
            current_groups.pop(tmpval)
            cutpop+=1


        return current_groups #random.choices(current_groups, weights=fitness, k=self.POP_SIZE)

    # 交叉
    def get_couple(self, group_list):  #变多了，孩子加进去了
        child_list = []
        count=self.POP_SIZE-len(group_list)  #要生成的新个体
        i=0
        while i<count:
            mom_random = random.randint(0,len(group_list)-1)
            while mom_random == i:
                mom_random = random.randint(0,len(group_list)-1)
            child_list.append(self.cross_couple(group_list[i],group_list[mom_random]))
            i+=1
            if i>=len(group_list):
                break
        if count-i>0: #没有够数，就随机生成
            tmppop = [self.getDNA() for i in range(count-i)]
            child_list.extend(tmppop)
        #tmp=[]
        #tmp.extend(group_list)
        #tmp.extend(list(i for i in child_list))
        return group_list+child_list

    # 产生子代
    def cross_couple(self, dad, mom):  #15煤层分开交叉
        cross_rate = random.random()
        child_a1 = []
        child_b1 = []
        child_a2 = []
        child_b2 = []
        child_c1=dad[2]
        child_c2=mom[2]
        result=[]
        if cross_rate < self.CROSS_RATE:#交换15
            child_a2 = mom[1]
            child_b2 = dad[1]
        else:
            child_a2 = dad[1]
            child_b2 = mom[1]
        cross_rate = random.random()
        if cross_rate < self.CROSS_RATE:  #交叉14,16（使用内部交叉，分组为前后半截）
            mid=int(len(dad[0])/2)
            cross_place = random.randint(0,mid-1)  #14,16煤层分割为两个队是从中间分的
            child_a1 = dad[0][mid:mid+cross_place] + dad[0][cross_place:mid]+dad[0][0:cross_place] + dad[0][mid+cross_place:]
            child_b1 = mom[0][mid:mid+cross_place] + mom[0][cross_place:mid]+mom[0][0:cross_place] + mom[0][mid+cross_place:]
        else:
            child_a1 = dad[0]
            child_b1 = mom[0]
        if cross_rate < self.CROSS_RATE:
            child_c1 = mom[2]
            child_c2 = dad[2]
        choose = random.random()  #返回一个后代
        if choose < 0.5:
            result=[child_a1,child_a2,child_c1]
        else:
            result=[child_b1,child_b2,child_c2]
        return result


    def crossover(self,pop):
        for i in range(len(pop)):
            if random.random() < self.CROSS_RATE:
                mom_index = random.randint(0,len(pop)-1)
                while mom_index == i:
                    mom_index = random.randint(0,len(pop)-1)
                for j in range(len(pop[i][0])):
                    if random.randint(0, 1) == 1:
                        pop[i][0][j],pop[mom_index][0][j] = pop[mom_index][0][j],pop[i][0][j]
        return pop

if __name__ == "__main__":
    ga=GA_C()
    ga.get_type_coal_list()
    ga.add_index()
    print(ga.coal_list_a)
    print(ga.coal_list_b)
    a = ga.getDNA()
    print(ga.a)
    print(ga.mutate([a,a,a]))
    # print(decode_gorup(a)[0].coal_seam_list)
    # print(decode_gorup(a)[2].coal_seam_list)
