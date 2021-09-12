__author__ = "Yu Bao"
__license__ = "All right"
__version__ = "0.1 beta"

#from pylab import mpl
import matplotlib as plt

#设置中文字体【黑体】
plt.rcParams['font.sans-serif'] = ['SimHei']
#解决图像保存时负号 '-' 显示为方框的问题
plt.rcParams['axes.unicode_minus'] = False

import numpy as np
import time
import datetime
import matplotlib.patches


class ganttchart:
    matplotlib.pyplot.rcdefaults() #恢复到缺省的配置
    fig, ax = matplotlib.pyplot.subplots()
    barHeight = 0.3
    yLabels = []
    xLabels = []
    xticks = []
    xticksMap = []
    roundValue = 2
    bars = []
    legends = []

    def getTimeStr(self, tick: float):  #同一天的，按秒
        milliseconds = (tick - int(tick))
        tickStr = time.strftime("%Y-%m-%d", time.localtime(tick))  # %H:%M:%S
        tickStr = tickStr + "." + str(round(milliseconds, self.roundValue)).split('.')[1]
        return tickStr

    def getTimeStrDay(self, tick: float):  #days
        days = (int(tick))
        tickStr = time.strftime("%Y-%m-%d", time.localtime(tick))  # %H:%M:%S
        #tickStr = tickStr + "." + str(round(days, self.roundValue)).split('.')[1]
        return tickStr

    def addTask(self, name, start: float, end: float, resource, color):
        _end = round(end, self.roundValue)
        _start = round(start, self.roundValue)

        bar = [name, _start, _end, resource, color]
        if bar not in self.bars:
            self.bars.append(bar)
            if name not in self.yLabels:
                self.yLabels.append(name)

            if _start not in self.xticksMap:
                self.xticksMap.append(_start)

            if _end not in self.xticksMap:
                self.xticksMap.append(_end)

        if [resource, color] not in self.legends:
            self.legends.append([resource, color])

    def show(self, title,loc='center low'):
        self.xticksMap.sort()
        for item in self.xticksMap:
            self.xticks.append(len(self.xticks))
            tickStr = self.getTimeStrDay(item)  #getTimeStr(item)
            if tickStr not in self.xLabels:
                self.xLabels.append(tickStr)

        for bar in self.bars:
            #self.ax.barh(bar[0], (self.xticksMap.index(bar[2]) - self.xticksMap.index(bar[1])),  height=self.barHeight,
            #             left=self.xticksMap.index(bar[1]), align='center', color=bar[4], ecolor='black')
             self.ax.barh(bar[0], (bar[2] - bar[1]),  height=self.barHeight,
                     left=bar[1]-self.bars[0][1], align='center', color=bar[4], ecolor='black')
        #self.ax.set_xticks(self.xticks)
        #self.ax.set_xticklabels(self.xLabels)
        xtickstemp=list(range(0,len(self.xticks),10))
        temp=[self.xticksMap[i]-self.xticksMap[0] for i in range(0,len(self.xticks),10)]

        #self.ax.ticks=self.ax.set_xticks([0,self.xticksMap[10]-self.xticksMap[0],self.xticksMap[20]-self.xticksMap[0],
        #                                  self.xticksMap[30]-self.xticksMap[0]])
        self.ax.ticks=self.ax.set_xticks(temp)
        labelsshow=[self.xLabels[x] for x in xtickstemp]
        self.ax.set_xticklabels(labelsshow, rotation=20)  #self.xLabels, rotation=20)
        self.ax.set_yticklabels(self.yLabels)
        self.ax.invert_yaxis()  # labels read top-to-bottom
        self.ax.set_xlabel(u'时间Time')
        self.ax.set_title(title)
        #box = self.ax.get_position()
        #self.ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
        # for legend in self.legends:
        plotLegends = []
        for legend in self.legends:
            plotLegends.append(matplotlib.patches.Patch(color=legend[1], label=legend[0]))
        if loc=='center low':
            matplotlib.pyplot.legend(handles=plotLegends,bbox_to_anchor=(0.25,0.2),ncol=3)
        elif loc=='upper right':
            matplotlib.pyplot.legend(handles=plotLegends,bbox_to_anchor=(0.36,0.86),ncol=3)
        # xy被注释图形内容位置坐标，xytext注释文本的位置坐标，color注释文本的颜色。arrowprops指示被注释内容的箭头的属性字典
        ispre=False  #True
        if(ispre):
            matplotlib.pyplot.annotate("插入的车辆", xy=((np.pi / 2)+45, 0.85), xytext=((np.pi / 2) + 3, 0.65), color="black", weight="bold",
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            matplotlib.pyplot.annotate("插入的车辆", xy=((np.pi / 2) + 75, 0.15), xytext=((np.pi / 2) + 3, 0.65), color="black",
                                       weight="bold",
                                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
            matplotlib.pyplot.annotate("减少的车辆", xy=((np.pi / 2) + 220, 0.15), xytext=((np.pi / 2) + 170, 0.3), color="black",
                                       weight="bold",
                                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="b"))
        matplotlib.pyplot.show()