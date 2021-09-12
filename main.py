''' @File :class_set.py
    @Author:baoyu
    @Date :2021/7/1 19:19
    @Desc : '''
import time
import pandas as pd
from class_set import *

from matplotlib import pyplot as plt
#from utils.timestamp import calculate_time
from utils.get_time import *
from utils.FitnessFun import FitnessFun
from utils.GA_class import *
import multiprocessing as mp
from utils.NSGAII import *

class resultDeal:
    def checkoutput(self,out, loc):  #loc=0表示年产量，=1表示年产量方差
        pud=PubData()
        result=False
        x=[i[loc] for i in out]
        if loc==0:
            tmp=x
            if pud.MultiProcess:
                tmp = [x[i][0] for i in range(len(x))]
            for i in tmp:
                if pud.StdProcdutionPerY*pud.minRatio<=i <=pud.StdProcdutionPerY*1.1:
                    result=True
                    break
        else:
            xx=sum([i[0] for i in out])**2
            for i in x:
                if i/xx<0.01  :  #是否是0.1还要确认
                    result=True
                    break
        return  result
    def analyzeResult(self,group):  #group 三个队伍编制，没循环一次一个当前循环最优的
        eachyearprdct=[]
        eachyeargangue=[]
        resultslist=[]  #1st-3rd 每年每队的产量，4 gangue产量
        timetable=[]    #1-2，队1的coallist序列和时间，3-4,5-6分别队2,3
        team1=list(map(lambda x:x[0],group))
        team2=list(map(lambda x:x[1],group))
        team3=list(map(lambda x:x[2],group))
        for i in range(len(team1)):
            resultslist.append((team1[i].eachyear_total))
            resultslist.append((team3[i].eachyear_total))
            resultslist.append((team2[i].eachyear_total))  #充填队
            resultslist.append((team1[i].gangueperyear))   #矸石
            resultslist.append((team3[i].gangueperyear))   #矸石
        df = pd.DataFrame(resultslist)
        df.to_excel("teamproduct.xlsx")

        for i in range(len(team1)):
            tmp1=[[] for i in range(9)]
            for j in team1[i].coal_seam_list:
                tmp1[0].append(j.name)
                if hasattr(j, 'begin_time'):
                    tmp1[1].append(j.begin_time)
                    if hasattr(j, 'end_time'):
                        tmp1[2].append(j.end_time)
                    elif j.advancing_length_backup!=j.advancing_length:
                            tmp1[2].append(get_time(j.begin_time, 330))
                else:
                    continue
            for j in team3[i].coal_seam_list:
                tmp1[3].append(j.name)
                if hasattr(j, 'begin_time'):
                    tmp1[4].append(j.begin_time)
                    if hasattr(j, 'end_time'):
                        tmp1[5].append(j.end_time)
                    elif j.advancing_length_backup!=j.advancing_length:
                        tmp1[5].append(get_time(j.begin_time,330))
                else:
                    continue
            for j in team2[i].coal_seam_list:
                tmp1[6].append(j.name)
                if hasattr(j, 'begin_time'):
                    tmp1[7].append(j.begin_time)
                    if hasattr(j, 'end_time'):
                        tmp1[8].append(j.end_time)
                    elif j.advancing_length_backup!=j.advancing_length:
                        tmp1[8].append(get_time(j.begin_time,330))
                else:
                    continue
            for i in range(9):
                timetable.append(tmp1[i])
        df1 = pd.DataFrame(timetable)
        df1.to_excel("timetable.xlsx")

if __name__ == "__main__":
    ga=GA_C()
    pud=PubData()
    fit=FitnessFun()
    fittype=0
    if pud.Method=='NSGAII':
        fittype= 7  #6 is diff+fillrate,7 is output+fillrate, 8 is min diff+fillrate
        ga=NSGAII()
    rd=resultDeal()
    # 生成DNA形成种群
    pop = [ga.getDNA() for i in range(ga.POP_SIZE)]
    if pud.MultiProcess:
        pool = mp.Pool(int(mp.cpu_count()))
    resultslist=[]  #存放了均产量
    groupresults=[]  #存放队伍
    start = time.time()
    i=0
    while i < ga.N_GENERATIONS:
        time.sleep(1)
        print(f"这是第{i}代")
        if  pud.MultiProcess:
            pud.MPtype=1
            decode_pop=[pool.apply_async(ga.decode_gorup,args=('task',pop[i:i+1])) for i in range(len(pop))] #for name,pdata in param_dict.items()]
            decode_pop=[p.get() for p in decode_pop]
            output = [pool.apply_async(fit.calculate_time, (pud.MPtype, decode_pop[i:i+1],)) for i in range(len(decode_pop))]
            output = [p.get() for p in output]
            group = list(map(lambda x: x[1], output))
            outputtmp=[output[i][0] for i in range(len(output))]
            groupresults.append(group[0])
        else:
            tmp=np.zeros(len(pop))
            decode_pop = list(map(ga.decode_gorup, str(tmp),pop))  # 初始化编码
            tmp=list(map(fit.calculate_time,tmp,decode_pop))
            group=list(map(lambda x:x[1],tmp))
            output = list(map(lambda x:x[0],tmp))
            outputtmp=output
            groupresults.append(group[0])
        print(outputtmp)
        resultslist.append(outputtmp[0])
        if (rd.checkoutput(output,0)):
            if pud.MultiProcess:
                if output[0][0][3]>ga.fillrateMin/100 and output[0][0][0]>pud.StdProcdutionPerY*pud.minRatio:  #第一次，没排序
                    ga.fillrateMin=output[0][0][3]*100  #如果发现有结果了，应该找更大的fillrate
                    if ga.fillrateMin>75:
                        ga.fillrateMin=75
                    ga.fillrateMax=output[0][0][3]*100+10
                    print(ga.fillrateMin,ga.fillrateMax)
            else:
                if output[0][3]>ga.fillrateMin/100:
                    ga.fillrateMin=output[0][3]*100  #如果发现有结果了，应该找更大的fillrate
                    ga.fillrateMax=output[0][3]*100+20
            print("ok====",output[0])
            #break
        #print(output)
        #plt.clf()
        #plt.plot(output)
        #plt.pause(0.1)
        #plt.ioff()
        # 获取适应度
        if pud.MultiProcess:
            fitness = ga.get_fitness([i[0] for i in output], fittype)
        else:
            fitness=ga.get_fitness(output, fittype)
        print(fitness)
        # 选择
        new_pop = ga.select(pop,fitness,fittype)  #选择可用的
        # 交叉
        cross_pop = ga.get_couple(new_pop) #ga.crossover(new_pop)  孩子加进去了
        # 变异
        pop = ga.mutate(cross_pop)
        #print(max(output),min(output))
        i+=1
    #decode_pop = list(map(ga.decode_gorup, pop))
    #output = list(map(ga.calculate_time, decode_pop))
    # write to excel
    rd.analyzeResult(groupresults) #分析结果，存储文件
    df = pd.DataFrame(resultslist)
    df.to_excel("results.xlsx")  #产量
    print("last output:", output)
    #plt.plot(output)  #最后作图
    end = time.time()
    print("time:", end - start, "s")
