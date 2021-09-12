''' @File :class_set.py
    @Author:baoyu
    @Date :2021/7/1 19:19
    @Desc : '''
"""
drawpic
"""
from datetime import datetime, timedelta
from utils import NSGAII
from class_set import *
from utils.get_time import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab as mpl
import utils.MyGanttchart as ganttchart
import time

#设置中文字体【黑体】
#mpl.rcParams['font.sans-serif'] = ['SimSun']
#解决图像保存时负号 '-' 显示为方框的问题
#mpl.rcParams['axes.unicode_minus'] = False


class DrawResults:
    def __init__(self):
        self.columns = []
        self.dataset = []
        self.filetype='Excel'  #or txt
        self.gc=ganttchart.ganttchart()
        self.pud=PubData()
        self.sch_time=pud.SCHEDULINGTIME


    def loadOutputDatafromexcel(self, filepath, sheet):#para: excel file name,
        data1 = pd.read_excel(filepath, sheet)
        self.dataset = np.array(data1)

    def loadYearsDatafromexcel(self, filepath, sheet):#para: excel file name,
        data1 = pd.read_excel(filepath, sheet)
        #data1 = data1.iloc[:,]  #切割列
        #data1.set_index(keys="路径")  排序
        self.df=data1
        self.dataset = np.array(data1)
    def loadTimeDatafromexcel(self, filepath, sheet):#para: excel file name,
        data1 = pd.read_excel(filepath, sheet)
        self.df2=data1
        self.dataset = np.array(data1)

    def drawoutline(self):
        x = []
        for i in range(1,len(self.dataset)):
            x.append(i)
        data1 = self.dataset[:, [1]]
        #data2 = self.dataset[1:, [3]]
        data3 = self.dataset[:, [4]]
        data1=np.delete(data1,0,0)
        data3=np.delete(data3, 0, 0)
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('iteration times')
        ax1.set_ylabel('production output', color='red')
        y1,=ax1.plot(x, data1, color='red')
        #ax1.plot(x, data2, '-*', color='green')
        #ax1.plot(x, data3, color='blue')
        ax1.tick_params(axis='y', labelcolor='red')

        plt.legend(labels=['output'], loc=(0.75,0.7), borderaxespad=0.)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel('filling rate', color='blue')
        ax2.plot(x, data3, color='blue')
        # plt.plot(self.dataset[:,2], '-*')
        ax2.tick_params(axis='y', labelcolor='blue')
        plt.grid(True)
        plt.title("the production output")
        plt.legend(labels=['filling rete'], loc=(0.7,0.2), borderaxespad=0.)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
    def drawHistoprogramProductionout(self,syears):
        tname=['Eteam1','Eteam2','Fteam3','total']
        x = np.arange(1,syears+1,1)    #生成x轴,每年一个
        y=[[] for i in range(syears)]
        y1 = [[] for i in range(syears)]
        for i in range(syears):  #读取y数据
            y[i]=self.df[i]

        y1=[list(y[i][len(y[i])-5:]) for i in range(len(y))]
        y2=[[] for i in range(len(y1[0]))]
        for j in range(len(y2)):
            y2[j]=[y1[i][j] for i in range(len(y1))]
        y3=[y2[0][i]+y2[1][i]+y2[2][i] for i in range(len(y2[0]))]
        y4 = [y2[3][i]+y2[4][i] for i in range(len(y2[0]))]
        # 设置图形大小
        plt.rcParams['figure.figsize'] = (7.0, 5.0)
        fig = plt.figure()
        # 画柱形图
        x1 = np.arange(len(x))
        #total_width, n = 0.8, len(self.df["Cname"])  # 有多少个类型，只需更改n即可
        width = 0.1  # total_width / (n-1)
        for i in range(3):
            plt.bar(x+ i*width, y2[i], width=width, label=tname[i])
        plt.bar(x + 3*width, y3, width=width, label='total')
        plt.bar(x + 4 * width, y4, width=width, label='gangue')

        my_x_ticks = np.arange(1, syears+1, 1)
        plt.xticks(my_x_ticks)
        plt.legend(loc="upper center", ncol=3)  # 防止label和图像重合显示不出来
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.ylabel('production output each year(t)')
        plt.xlabel('years')
        plt.rcParams['savefig.dpi'] = 300  # 图片像素
        plt.rcParams['figure.dpi'] = 300  # 分辨率
        # plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
        plt.title("Optimal production output each year")
        # plt.savefig('D:\\result.png')
        plt.show()

    def drawtimetable(self,syears):  #time's gantt fig,搬家时间ji14,15,16 are 40,51,37
        tname=['Eteam1','Eteam2','Fteam3']
        twait=[40,51,37]
        x = np.arange(0,syears,1)    #生成x轴,每年一个
        y=[[] for i in range(syears)]
        y0=[[] for i in range(syears)]

        for i in range(syears):  #读取y数据
            y[i]=self.df2[i]

        y0=[list(y[i][len(y[i])-9:]) for i in range(len(y))]  #3 groups and 3 rows each,first row is name

        #for j in range(len(y0)):  #name,begin_time,end_time
        y1=[y0[i][0:3] for i in range(len(y0))]
        y2 = [y0[i][3:6] for i in range(len(y0))]
        y3 = [y0[i][6:9] for i in range(len(y0))]

        # 设置图形大小
        #plt.rcParams['figure.figsize'] = (7.0, 5.0)
        #fig = plt.figure()

        x4 = ""
        x5 = ""
        for i in range(len(y1)-1):
            x1 = str(tname[0])
            if y1[i][1] != y1[i][1]:  # is nan
                break
            x2 = time.mktime(time.strptime(y1[i][1].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x3 = y1[i][2]
            x31=x3   #x3现在包含搬家时间
            x22=x32=None
            if str(y1[i][0])[0] == "3":
                x3=sub_time(y1[i][2],twait[0])
                x4 = "ji-14"
                x5 = "blue"
            elif str(y1[i][0])[0]== "6":
                x3 = sub_time(y1[i][2], twait[2])
                x4 = "ji-16"
                x5 = "darkblue"
            x21 = x3
            x3 = time.mktime(time.strptime(x3.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            self.gc.addTask(x1, x2, x3, x4, x5)
            #x2 = y1[2][i]
            #x3 = get_time(y1[2][i],twait[1])
            x21=time.mktime(time.strptime(x21.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x31 = time.mktime(time.strptime(x31.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x4 = "moving"
            x5 = "yellow"
            self.gc.addTask(x1, x21, x31, x4, x5)
        for i in range(len(y2)-1):
            x1 = str(tname[1])
            if y2[i][1]!=y2[i][1]:  #is nan
                break
            x2 = time.mktime(time.strptime(y2[i][1].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x3 = y2[i][2]
            x31=x3   #x3现在包含搬家时间
            x22=x32=None
            if str(y2[i][0])[0] == "3":
                x3=sub_time(y2[i][2],twait[0])
                x4 = "ji-14"
                x5 = "blue"
            elif str(y2[i][0])[0]== "6":
                x3 = sub_time(y2[i][2], twait[2])
                x4 = "ji-16"
                x5 = "darkblue"
            x21 = x3
            x3 = time.mktime(time.strptime(x3.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            self.gc.addTask(x1, x2, x3, x4, x5)
            #x2 = y1[2][i]
            #x3 = get_time(y1[2][i],twait[1])
            x21=time.mktime(time.strptime(x21.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x31 = time.mktime(time.strptime(x31.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x4 = "moving"
            x5 = "yellow"
            self.gc.addTask(x1, x21, x31, x4, x5)
        for i in range(len(y3)-1):   #充填队中endtime没有搬家时间
            x1 = str(tname[2])
            if i>0 and y3[i][1]==y3[i][1]:  #不是第一个，有抽采时间   gas
                x22 = get_time(y3[i-1][2], twait[1])
                if y3[i][1] > x22: #存在gas时间
                    if get_time(x22,self.pud.GASExtractionTime)<y3[i][1]:
                        x22=sub_time(y3[i][1],self.pud.GASExtractionTime)
                    x32 = y3[i][1]
                    if x32 == x32:  # not none
                        #x32 = sub_time(x32, self.pud.GASExtractionTime)
                        x22 = time.mktime(time.strptime(x22.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x32 = time.mktime(time.strptime(x32.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x4 = "Gas"
                        x5 = "plum"
                        self.gc.addTask(x1, x22, x32, x4, x5)  # gas
            #working
            if y3[i][1]!=y3[i][1]:  #is nan
                break
            x2 = time.mktime(time.strptime(y3[i][1].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x3 = y3[i][2]
            if str(y3[i][0])[0] == "5":
                x3=time.mktime(time.strptime(y3[i][2].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                x4 = "ji-15"
                x5 = "green"
            self.gc.addTask(x1, x2, x3, x4, x5)  #ji15，working
            #moving
            x21 = y3[i][2]
            x31=get_time(x21,twait[1])
            x21=time.mktime(time.strptime(x21.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x31 = time.mktime(time.strptime(x31.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x4 = "moving"
            x5 = "yellow"
            self.gc.addTask(x1, x21, x31, x4, x5)  #move devices
            #waiting
            if i>0 and (y3[i][2]==y3[i][2] and y3[i+1][1]==y3[i+1][1]):  #不是第一个，有抽采时间   gas
                x23=get_time(y3[i][2],self.pud.GASExtractionTime)
                if y3[i+1][1]>x23:
                    x23=get_time(y3[i][2],twait[1])
                    x33 = sub_time(y3[i+1][1],self.pud.GASExtractionTime)
                    if x33==x33:
                        x23 =time.mktime(time.strptime(x23.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x33= time.mktime(time.strptime(x33.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x4 = "waiting"
                        x5 = "gray"
                        self.gc.addTask(x1, x23, x33, x4, x5)

        self.gc.show(u'Time table for each team arragement')
    def drawblocktimetable(self,syears):  #time's gantt fig,搬家时间ji14,15,16 are 40,51,37
        #tname=['Eteam1','Eteam2','Fteam3']
        twait=[40,51,37]
        x = np.arange(0,syears,1)    #生成x轴,每年一个
        y=[[] for i in range(syears)]
        y0=[[] for i in range(syears)]

        for i in range(syears):  #读取y数据
            y[i]=self.df2[i]

        y0=[list(y[i][len(y[i])-9:]) for i in range(len(y))]  #3 groups and 3 rows each,first row is name

        #for j in range(len(y0)):  #name,begin_time,end_time
        y1=[y0[i][0:3] for i in range(len(y0))]
        y2 = [y0[i][3:6] for i in range(len(y0))]
        y3 = [y0[i][6:9] for i in range(len(y0))]

        # 设置图形大小
        #plt.rcParams['figure.figsize'] = (7.0, 5.0)
        #fig = plt.figure()

        x4 = ""
        x5 = ""
        for i in range(len(y1)-1):
            x1 = str(y1[i][0])
            if y1[i][1] != y1[i][1]:  # is nan
                break
            x2 = time.mktime(time.strptime(y1[i][1].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x3 = y1[i][2]
            x31=x3   #x3现在包含搬家时间
            x22=x32=None
            if str(y1[i][0])[0] == "3":
                x3=sub_time(y1[i][2],twait[0])
                x4 = "ji-14"
                x5 = "blue"
            elif str(y1[i][0])[0]== "6":
                x3 = sub_time(y1[i][2], twait[2])
                x4 = "ji-16"
                x5 = "darkblue"
            x21 = x3
            x3 = time.mktime(time.strptime(x3.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            self.gc.addTask(x1, x2, x3, x4, x5)
            #x2 = y1[2][i]
            #x3 = get_time(y1[2][i],twait[1])
            x21=time.mktime(time.strptime(x21.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x31 = time.mktime(time.strptime(x31.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x4 = "moving"
            x5 = "yellow"
            self.gc.addTask(x1, x21, x31, x4, x5)
        for i in range(len(y2)-1):
            x1 = str(y2[i][0])  #name
            if y2[i][1]!=y2[i][1]:  #is nan
                break
            x2 = time.mktime(time.strptime(y2[i][1].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x3 = y2[i][2]
            x31=x3   #x3现在包含搬家时间
            x22=x32=None
            if str(y2[i][0])[0] == "3":
                x3=sub_time(y2[i][2],twait[0])
                x4 = "ji-14"
                x5 = "blue"
            elif str(y2[i][0])[0]== "6":
                x3 = sub_time(y2[i][2], twait[2])
                x4 = "ji-16"
                x5 = "darkblue"
            x21 = x3
            x3 = time.mktime(time.strptime(x3.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            self.gc.addTask(x1, x2, x3, x4, x5)
            #x2 = y1[2][i]
            #x3 = get_time(y1[2][i],twait[1])
            x21=time.mktime(time.strptime(x21.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x31 = time.mktime(time.strptime(x31.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x4 = "moving"
            x5 = "yellow"
            self.gc.addTask(x1, x21, x31, x4, x5)
        for i in range(len(y3)-1):   #充填队中endtime没有搬家时间
            x1 = str(y3[i][0])  #name
            if y3[i][1]!=y3[i][1]:  #is nan
                break
            if i>0:  #不是第一个，有抽采时间   gas
                x22 = get_time(y3[i-1][2], twait[1])
                if y3[i][1] > x22: #存在gas时间
                    if get_time(x22,self.pud.GASExtractionTime)<y3[i][1]:
                        x22=sub_time(y3[i][1],self.pud.GASExtractionTime)
                    x32 = y3[i][1]
                    if x32 == x32:  # not none
                        #x32 = sub_time(x32, self.pud.GASExtractionTime)
                        x22 = time.mktime(time.strptime(x22.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x32 = time.mktime(time.strptime(x32.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x4 = "Gas"
                        x5 = "plum"
                        self.gc.addTask(x1, x22, x32, x4, x5)  # gas
            #working
            x2 = time.mktime(time.strptime(y3[i][1].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x3 = y3[i][2]
            if str(y3[i][0])[0] == "5":
                x3=time.mktime(time.strptime(y3[i][2].strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                x4 = "ji-15"
                x5 = "green"
            self.gc.addTask(x1, x2, x3, x4, x5)  #ji15，working
            #moving
            x21 = y3[i][2]
            x31=get_time(x21,twait[1])
            x21=time.mktime(time.strptime(x21.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x31 = time.mktime(time.strptime(x31.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
            x4 = "moving"
            x5 = "yellow"
            self.gc.addTask(x1, x21, x31, x4, x5)  #move devices
            #waiting
            if i>0 and (y3[i][2]==y3[i][2] and y3[i+1][1]==y3[i+1][1]):  #不是第一个，有抽采时间   gas
                x23=get_time(y3[i][2],self.pud.GASExtractionTime)
                if y3[i+1][1]>x23:
                    x23=get_time(y3[i][2],twait[1])
                    x33 = sub_time(y3[i+1][1],self.pud.GASExtractionTime)
                    if x33==x33:
                        x23 =time.mktime(time.strptime(x23.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x33= time.mktime(time.strptime(x33.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
                        x4 = "waiting"
                        x5 = "gray"
                        self.gc.addTask(x1, x23, x33, x4, x5)

        self.gc.show(u'Time table for each team arragement',loc='upper right')
if __name__ == '__main__':  #
    pud=PubData()
    schedulingyears=10 #pud.SCHEDULINGTIME
    drawpic=DrawResults()
    #drawpic.loadOutputDatafromexcel("./results.xlsx","Sheet1")  #产量
    #drawpic.drawoutline()
    #drawpic.loadYearsDatafromexcel("./teamproduct15.xlsx", "Sheet1")  # year产量
    #drawpic.drawHistoprogramProductionout(schedulingyears)
    drawpic.loadTimeDatafromexcel("./timetable15.xlsx", "Sheet1")  # year产量
    #drawpic.drawtimetable(schedulingyears)  #timetable
    drawpic.drawblocktimetable(schedulingyears)