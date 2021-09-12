''' @File :class_set.py
    @Author:baoyu
    @Date :2021/7/1 19:19
    @Desc : '''
import pandas as pd
import random
import copy
import  numpy as np
from class_set import *



class NSGAII:
    def __init__(self):
        pud=PubData()
        self.coal_list_a= []  # 综采队列表
        self.coal_list_c = []  # 综采队列表
        self.coal_list_b= []  # 填充队列表
        self.CROSS_RATE = 0.8
        self.CROSS_COUNT = 3
        self.COAL_14_16_MUTATION_RATE = 0.5
        self.COAL_15_MUTATION_RATE = 0.5
        self.FILLRATE_MUTATION_RATE = 0.5
        self.POP_SIZE = pud.POPSIZE #40
        self.NEWPOP_PERTIME=0.3  #每次选择后，重新生成的替换比例
        self.N_GENERATIONS = pud.N_GENERATIONS
        self.Method=pud.Method
        self.fillTeamNum=2  #充填队数目
        self.ExpTeamNum = 2  #综采对数目
        self.SelectedProb=0.4  #选择去除的概率
        self.SaveGoodRate=0.3
        self.GASExtractionTime=pud.GASExtractionTime
        self.fillratevalue=0.5
        self.FitnessType=pud.FitnessType  #使用目标函数的类型，产量或均方差
        self.get_type_coal_list() # 初始化数据读入
        self.add_index()  #添加充填层15层前后序的索引
        self.fillrateMin=30
        self.fillrateMax = 75
        self.StdProcdutionPerY=pud.StdProcdutionPerY*0.9
        self.fillrateset=[0.95,0.9,0.85,0.8,0.75,0.7,0.65,0.6,0.55,0.5,0.45,0.4,0.35,0.3]


    def get_type_coal_list(self):
        """
        :return:三种煤层的列表
        """
        data = pd.read_excel(r"PeiCai.xlsx")  #data = pd.read_excel(r"PeiCai 的副本.xlsx")
        prev_data = pd.read_excel(r"十二矿煤层层位表.xlsx", 1)

        for index, row in data.iterrows():
            a = []
            for _, col in row.iteritems():
                a.append(col)
            coal = Coal(*a)  #取coal数据
            coal.advancing_length_backup=coal.advancing_length  #备份一下，最后检查是否开采过
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
                if coal.name != 631030:  #可以直接采，要不要str？
                    self.coal_list_c.append(coal)
                else:
                    self.coal_list_c.insert(0, coal)
            elif coal.mining_status == '未采' and coal.coal_seam == '己14煤层':
                if coal.name != 31040:
                    self.coal_list_a.append(coal)
                else:
                    self.coal_list_a.insert(0,coal)
            elif coal.mining_status == '未采' and coal.coal_seam == '己15煤层':
                if coal.name == 531070:  #首采工作面要进行处理,最后返回时添加，原来的是31020，但是需要等待
                    self.coal_list_b = [coal] + self.coal_list_b
                else:
                    self.coal_list_b.append(coal)
        self.InsertGasTime(self.coal_list_b,self.coal_list_a)
        self.coal_list_a.extend(self.coal_list_c)

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
        for i in self.coal_list_b:
            for index, j in enumerate(self.coal_list_a):
                if i.prev and j.coal_seam == "己14煤层" and j.name in i.prev:
                    i.prev_index.append(index)
        for index, m in enumerate(self.coal_list_a):
            if m.coal_seam == "己14煤层":
                continue
            for n in self.coal_list_b:
                if m.prev and m.coal_seam == "己16-17煤层" and n.name in m.prev:
                    n.back_index.append(index)


    # 15煤的基因编码
    def get_code_15(self):
        """
        返回的是[0,1,2,3,4,....]代表下标的列表
        :return:
        """
        code_15=[]
        #code_15 = list(range(1, len(coal_list_b)))
        for index in enumerate(self.coal_list_b):
            code_15.append(index[1].name)
        # 给15煤打乱顺序
        random.shuffle(code_15[1:])  #随机排序,首采面不懂
        #需要定首采面（暂时没有用，因为也压煤）
        return code_15   #0?     原来有[0] +


    def getDNA(self):
        """
        :return: 返回随机的一个样本
        """
        code_15 = self.get_code_15()
        code_1416 = []
        len_1416 = len(self.coal_list_a)
        #for i in range(len_1416):
        #    code_1416.append(random.randint(0, 1))
        for index in enumerate(self.coal_list_a):
            if index[1].name!=631030 and index[1].name !=31040:
                code_1416.append(index[1].name)
        random.shuffle(code_1416)  # 随机排序
        #code_15.insert(0,531070) #在get_code_15处理
        code_1416.insert(int(len(code_1416)/2),631030)
        code_1416.insert(0,31040)
        self.CreateFillRate()  # 随机充实率
        return [code_1416, code_15, self.fillratevalue]


    def CreateFillRate(self):
        self.fillratevalue = random.randint(self.fillrateMin,self.fillrateMax)/100  # 随机充实率
        return self.fillratevalue
    def CreateFillRate2(self): #从集合中随机抽取一个
        return random.choice(self.fillrateset)
    def decode_gorup(self,name, DNA):
        """
        :param DNA:
        :return: 返回解码后的group
        """
        # 不备份的话不同样本之间会干扰
        coal_list_a_backup = copy.deepcopy(self.coal_list_a)
        if(len(name)>2):
            DNA=DNA[0]
        decode_coal_15_list = []
        decode_mining_team1_list = []
        decode_mining_team2_list = []
        #facecount=0
        for i in range(len(DNA[1])):
            #if facecount % 2==0:
            self.coal_list_b[i].team = 0  #充填队的编号设定为0和1，相当于只有一个充填队不间断工作
            #else:
            #    coal_list_b[i].team=1
            #facecount=facecount+1

            decode_coal_15_list.append(DNA[1][i])

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
            for j in self.coal_list_a:
                if str(j.name)==str(decode_mining_team1_list[i]):
                    tmp=copy.deepcopy(j)
                    decode_mining_team1_list_tmp.append(tmp)
                    break
        for i in range(len(decode_mining_team2_list)):  #充填队转码
            for j in self.coal_list_a:
                if str(j.name)==str(decode_mining_team2_list[i]):
                    tmp = copy.deepcopy(j)
                    decode_mining_team2_list_tmp.append(tmp)
                    break
        for i in range(len(decode_coal_15_list)):  #充填队转码
            for j in self.coal_list_b:
                if str(j.name)==str(decode_coal_15_list[i]):
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
        elif type==6:  #NSGAII,单进程，方差+充实率
            tmp = [(average_annual_output[i][2],average_annual_output[i][3]) for i in range(len(average_annual_output))]
        elif type == 7:  # NSGAII,产量+充实率
            tmp = [(average_annual_output[i][0], average_annual_output[i][3]) for i in
                   range(len(average_annual_output))]
        elif type == 8:  # NSGAII,最小年产量+充实率
            tmp = [(average_annual_output[i][2], average_annual_output[i][3],average_annual_output[i][0]) for i in
                   range(len(average_annual_output))]
        #if total==0:
        #    return [0.1 for i in tmp]
        #return [i/total for i in tmp]
        return tmp

    def mykeycmp(self,elem):
        return elem[1]
    def select(self,current_groups,fitness,fittype):
        """
        选择样本,按照概率选择即可   random.choice
        :param current_groups:当前所有的样本分组 [group1,group2,....,groupn]
        :param fitness: 适应度
        :return: 返回选择后的新样本
        """
        tmp=[]
        tmpp=[]
        tmp = sorted(zip(fitness, current_groups), reverse=True)  # 两个list关联排序,只能一次，奇怪
        if self.FitnessType == 2:
            tmp = sorted(zip(fitness, current_groups))
        fitness, current_groups = zip(*tmp)
        if self.Method=='NSGAII': #多目标优化(应该分成两个部分，满足产量的和不满足的）
            if(fittype==6):
                current_groups,fitness=self.fast_non_dominated_sort(current_groups,fitness,fittype)
            elif(fittype==7):
                proloc=0
                for i in range(len(fitness)):
                    if fitness[i][0]>=self.StdProcdutionPerY: #如果不能达产，按照产量找，达产之后才均衡
                        proloc+=1   #找到所有达产的最后一个位置
                if proloc>0:
                    current_groups1, fitness1 = self.fast_non_dominated_sort(current_groups[:proloc], fitness[:proloc], fittype)
                    current_groups, fitness = self.fast_non_dominated_sort(current_groups[proloc:], fitness[proloc:],fittype)
                    current_groups=current_groups+current_groups1
                    fitness=fitness+fitness1
                else:
                    current_groups, fitness = self.fast_non_dominated_sort(current_groups, fitness,fittype)
            elif fittype==8:
                proloc=0
                for i in range(len(fitness)):
                    if fitness[i][0]>=self.StdProcdutionPerY: #如果不能达产，按照产量找，达产之后才均衡
                        proloc+=1   #找到所有达产的最后一个位置
                if proloc>0:
                    current_groups1, fitness1 = self.fast_non_dominated_sort(current_groups[:proloc], fitness[:proloc], fittype)
                    current_groups, fitness = self.fast_non_dominated_sort(current_groups[proloc:], fitness[proloc:],fittype)
                    current_groups=current_groups+current_groups1
                    fitness=fitness+fitness1

        #        else:
        #            tmp = sorted(zip(fitness, current_groups), reverse=True)  # 两个list关联排序,只能一次，奇怪
        #            if self.FitnessType == 2:
        #                tmp = sorted(zip(fitness, current_groups))
        #            fitness, current_groups = zip(*tmp)
        #else:  #单目标优化
        #    tmp=sorted(zip(fitness,current_groups),reverse=True)  #两个list关联排序,只能一次，奇怪
        #    if self.FitnessType==2:
        #        tmp = sorted(zip(fitness, current_groups))
        #    fitness,current_groups=zip(*tmp)

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
            if self.Method == 'NSGAII':  # 多目标优化
                fitness.pop(-1)
                current_groups.pop(-1)
            else:
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
        while i<count and len(group_list)>1:
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

    #Function to carry out NSGA-II's fast non dominated sort
    def fast_non_dominated_sort(self,pop, fitness,fittype):  #pop is chromo and fitness is values list
        values1=[fitness[i][0] for i in range(0,len(fitness))]
        values2=[fitness[i][1] for i in range(0,len(fitness))]
        S=[[] for i in range(0,len(values1))]
        sp=[]
        sf=[]
        front = [[]]
        n=[0 for i in range(0,len(values1))]
        rank = [0 for i in range(0, len(values1))]
        if fittype==6:
            for p in range(0,len(values1)):
                S[p]=[]
                n[p]=0   #第几层
                for q in range(0, len(values1)):
                    if (values1[p] <= values1[q] and values2[p] >= values2[q]):
                        if q not in S[p]: #in sset:   #
                            S[p].append(q)  #得到序号
                    elif (values1[q] <= values1[p] and values2[q] >=values2[p]):
                        n[p] = n[p] + 1
                if n[p]==0:
                    rank[p] = 0
                    if p not in front[0]:
                        front[0].append(p)
                        sf.append(fitness[p])  # 添加排序序列
                        sp.append(pop[p])
        elif fittype==7:  #不同type，不同比较方式
            for p in range(0,len(values1)):
                S[p]=[]
                n[p]=0   #第几层
                for q in range(0, len(values1)):
                    if (values1[p] >= values1[q] and values2[p] >= values2[q]):
                        if q not in S[p]: #in sset:   #
                            S[p].append(q)  #得到序号
                    elif (values1[q] >= values1[p] and values2[q] >=values2[p]):
                        n[p] = n[p] + 1
                if n[p]==0:
                    rank[p] = 0
                    if p not in front[0]:
                        front[0].append(p)
                        sf.append(fitness[p])  # 添加排序序列
                        sp.append(pop[p])
        #在进行同等级pareto排序
        startp=0
        i = 0
        while(front[i] != []):
            Q=[]
            for p in front[i]:
                for q in S[p]:
                    n[q] =n[q] - 1
                    if( n[q]==0):
                        rank[q]=i+1
                        if q not in Q:
                            Q.append(q)
                            sf.append(fitness[q])  # 添加排序序列
                            sp.append(pop[q])
            i = i+1
            front.append(Q)
        del front[len(front)-1]
        spr=[]
        sfr=[]
        for i in range(len(front)):  #按照拥挤度排序
            sptmp,sftmp=self.crowding_distance_sorted_pro(sp,sf,startp,len(front[i]))
            spr.extend(sptmp)
            sfr.extend(sftmp)
            startp+=len(front[i])
        return spr,sfr
    #crowd 产量优先
    def crowding_distance_sorted_pro(self,pop,fitness,start, paretolen):  #paretolist当前level的长度,dis每次都要重算呀
        if paretolen==1:
            return pop,fitness
        minx1=min([x[0] for x in fitness[start:start+paretolen]])
        maxx2=max([x[0] for x in fitness[start:start+paretolen]])
        miny1=min([x[1] for x in fitness[start:start+paretolen]])
        maxy2=max([x[1] for x in fitness[start:start+paretolen]])
        X=maxx2-minx1
        Y=maxy2-miny1
        distance = [() for i in range(paretolen)]
        if fitness[start][0]>=self.StdProcdutionPerY:
            distance[0] = (abs(X + Y)+1, 0)
        else:
            distance[0]=(abs(X+Y),0)
        distance[paretolen-1]=(abs(X+Y),paretolen-1)
        for k in range(1,paretolen-1):
            if(fitness[start+k][0]>=self.StdProcdutionPerY): #如果产量合格，需要提高
                #distance[k]=2*(abs(fitness[start+k-1][0] - fitness[start+k+1][0])/X+abs(fitness[start+k-1][1] - fitness[start+k+1][1])/Y,k)
                #distance[k]=(1+fitness[start+k][1] ,k)  产量满足的pareto
                distance[k] = (abs(fitness[start + k - 1][0] - fitness[start + k + 1][0]) / X + abs(
                    fitness[start + k - 1][1] - fitness[start + k + 1][1]) / Y, k)
            else:
                if X==0 or Y==0:
                    distance[k]=(1,k)
                else:
                    #distance[k]=(abs(fitness[start+k-1][0] - fitness[start+k+1][0])/X+abs(fitness[start+k-1][1] - fitness[start+k+1][1])/Y,k)
                    distance[k] = (abs(fitness[start + k - 1][0] - fitness[start + k + 1][0]) / X *0.8+ abs(
                        fitness[start + k - 1][1] - fitness[start + k + 1][1]) / Y*0.2, k)
        poptmp = []
        fittmp = []
        distance=sorted(distance,key=lambda x:x[0],reverse=True)
        for i in range(paretolen):  #按照排序结果，创建新序列返回
            p=distance[i][1]
            poptmp.append(pop[start+p])
            fittmp.append(fitness[start+p])

        return poptmp,fittmp
    #crowding compute
    def crowding_distance_sorted(self,pop,fitness,start, paretolen):  #paretolist当前level的长度,dis每次都要重算呀
        if paretolen==1:
            return pop,fitness
        minx1=min([x[0] for x in fitness[start:start+paretolen]])
        maxx2=max([x[0] for x in fitness[start:start+paretolen]])
        miny1=min([x[1] for x in fitness[start:start+paretolen]])
        maxy2=max([x[1] for x in fitness[start:start+paretolen]])
        X=maxx2-minx1
        Y=maxy2-miny1
        distance = [() for i in range(paretolen)]
        distance[0]=(abs(X+Y),0)
        distance[paretolen-1]=(abs(X+Y),paretolen-1)
        for k in range(1,paretolen-1):
            distance[k]=(abs(fitness[start+k-1][0] - fitness[start+k+1][0])/X+abs(fitness[start+k-1][1] - fitness[start+k+1][1])/Y,k)
        distance=sorted(distance,key=lambda x:x[0],reverse=True)
        poptmp=[]
        fittmp=[]
        for i in range(paretolen):  #按照排序结果，创建新序列返回
            p=distance[i][1]
            poptmp.append(pop[start+p])
            fittmp.append(fitness[start+p])
        return poptmp,fittmp

    def testDNA(self):
        code_1416=['31180','31080','31200','31160','31280','31240','31260','631040','631160','631080','631180']
        code_1416.extend(['31040','31060','31100','31110','31140','631050','31130','631020','31120','631100','631030'])
        code_15=['531040','531020','531140','531080','531160','531070','531120']
        return [code_1416, code_15, 0.34]
