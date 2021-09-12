import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas import Series, DataFrame
import  numpy as np
import pylab as mpl

#设置中文字体【黑体】
mpl.rcParams['font.sans-serif'] = ['SimSun']
#解决图像保存时负号 '-' 显示为方框的问题
mpl.rcParams['axes.unicode_minus'] = False

class DrawResults():
    def __init__(self):
        self.columns=[]

    def loadData(self):
        self.columns.append("Integration")

    def loadDataFromExcel(self):  #cvs, xls
        self.df=pd.read_excel(r"./trucks.xlsx","cnnpath") #"lstmpath")
        ds=[]
        return ds

    # https://blog.csdn.net/qq_41479464/article/details/82830605
    def drawHistoprogrambyMatplot(self):
        x=self.df["Cname"]
        y1=self.df["ACC"]
        y2=self.df["F1"]
        y3 = self.df["Devi"]
        # 设置图形大小
        plt.rcParams['figure.figsize'] = (7.0, 5.0)
        fig = plt.figure()
        # 画柱形图
        x1 = np.arange(len(x))
        total_width, n = 0.8, len(self.df["Cname"])  # 有多少个类型，只需更改n即可
        width =0.3# total_width / (n-1)
        plt.bar(x, y1, width=width, label='ACC', color='red')
        plt.bar(x1 + width, y2, width=width, label='Fscore', color='darkblue')
        plt.bar(x1 + 2*width, y3, width=width, label='Devi', color='green')

        plt.xticks()
        plt.legend(loc="upper left",ncol=2)  # 防止label和图像重合显示不出来
        #plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.ylabel('Value(%)')
        plt.xlabel('不同深度的LSTM方法和偏离距离')
        plt.rcParams['savefig.dpi'] = 300  # 图片像素
        plt.rcParams['figure.dpi'] = 300  # 分辨率
        #plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
        plt.title("不同深度的LSTM方法和输出偏离")
        #plt.savefig('D:\\result.png')
        plt.show()
    def drawHistoprogrambyMatplotFordiffpath(self):  #对不同路径绘制
        x=self.df["Cname"]
        y1=self.df["ACC"]
        y2=self.df["F1"]
        y3 = self.df["Devi"]
        # 设置图形大小
        plt.rcParams['figure.figsize'] = (7.0, 5.0)
        fig = plt.figure()
        # 画柱形图
        x1 = np.arange(len(x))
        total_width, n = 0.8, len(self.df["Cname"])  # 有多少个类型，只需更改n即可
        width =0.3# total_width / (n-1)
        plt.bar(x, y1, width=width, label='ACC', color='red')
        plt.bar(x1 + width, y2, width=width, label='Fscore', color='darkblue')
        plt.bar(x1 + 2*width, y3, width=width, label='Devi', color='green')

        plt.xticks()
        plt.legend(loc="upper right",ncol=2)  # 防止label和图像重合显示不出来
        #plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.ylabel('Value(%)')
        plt.xlabel('LSTM模型泛化能力')
        plt.rcParams['savefig.dpi'] = 300  # 图片像素
        plt.rcParams['figure.dpi'] = 300  # 分辨率
        #plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
        plt.title("不同路径上的LSTM测试结果")
        #plt.savefig('D:\\result.png')
        plt.show()
    def drawHistoprogrambyMatplotForcmp(self):  #对不同路径绘制
        x=self.df["Cname"]
        y1=self.df["ACC"]
        y2=self.df["F1"]
        y3 = self.df["Devi"]
        # 设置图形大小
        plt.rcParams['figure.figsize'] = (7.0, 5.0)
        fig = plt.figure()
        # 画柱形图
        x1 = np.arange(len(x))
        total_width, n = 0.8, len(self.df["Cname"])  # 有多少个类型，只需更改n即可
        width =0.3# total_width / (n-1)
        plt.bar(x, y1, width=width, label='ACC', color='red')
        plt.bar(x1 + width, y2, width=width, label='Fscore', color='darkblue')
        plt.bar(x1 + 2*width, y3, width=width, label='Devi', color='green')

        plt.xticks()
        plt.grid()
        plt.legend(loc="upper left",ncol=1)  # 防止label和图像重合显示不出来
        #plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.ylabel('Value(%)')
        plt.xlabel('CNN模型类别')
        plt.rcParams['savefig.dpi'] = 300  # 图片像素
        plt.rcParams['figure.dpi'] = 300  # 分辨率
        #plt.rcParams['figure.figsize'] = (15.0, 8.0)  # 尺寸
        plt.title("CNN预测模型泛化能力")
        #plt.savefig('D:\\result.png')
        plt.show()
    def drawHistoprogrambySeaborn(self):
        x=self.df["Cname"]
        y1=self.df["ACC"]
        y2=self.df["F1"]
        # 设置图形大小
        plt.rcParams['figure.figsize'] = (12.0, 5.0)
        fig = plt.figure()
        # 画柱形图
        ax1 = fig.add_subplot(111)
        ax = sns.barplot(data=self.df, x='Cname',y='ACC')
        ax.legend(loc=8, ncol=3, framealpha=1, title='cat_var2')
        # ax1.set_title("数据统计",fontsize='20')
        # 画折线图
        ax2 = ax1.twinx()  # 组合图必须加这个
        ax2.plot(x, y2, 'r', ms=10)
        ax2.set_ylabel('N50', fontsize='15')
        plt.show()
    def drawbox(self):
        coe=1500
        list0=np.array([4.994e-5,9.96e-5,7.05e-5,1.0e-4,9.99e-5])*np.array([coe])
        list1=np.array([9.99e-5,9.99e-5,7.5e-5,1e-4,1.25e-4])*np.array([coe])
        list2=np.array([1.25e-4,1.25e-4,1.3e-4,1.3e-4,1.3e-4])*np.array([coe])
        list3=np.array([2.75e-4,2.75e-4,2.75e-4,2.75e-4,3e-4])*np.array([coe])
        list4=np.array([5.4e-5,1.3e-4,1.3e-4,7.35e-5,1.3e-4])*np.array([coe])
        list5=np.array([1.1e-4,1.3e-4,5.4e-4,2.116e-4,1.3e-4])*np.array([coe])
        data={
            '1D-LeNet-5':list0,
            'CPCNN4': list1,
            'CNCNN5': list2,
            '1D-AlexNet': list3,
            'DAE':list4,
            'GAM':list5

        }
        df=pd.DataFrame(data)
        df.plot.box(title="time of evaluation one compression")
        plt.grid(linestyle="--",alpha=0.4)
        plt.xlabel("Methods")
        plt.ylabel("time (s)")
        plt.show()
    def drawbox2(self):
        coe=1500
        list0=np.array([9.894e-5,2.66e-4,9.05e-5,1.01e-4,1.99e-4])*np.array([coe])
        list1=np.array([2.99e-4,1.1e-4,2.5e-4,1.3e-4,1.27e-4])*np.array([coe])
        list2=np.array([3.65e-4,4.65e-4,3.69e-4,3.71e-4,2.95e-4])*np.array([coe])
        list3=np.array([4.75e-4,4.95e-4,5.75e-4,4.75e-4,4.98e-4])*np.array([coe])
        list4=np.array([4.4e-4,3.3e-4,3.3e-4,3.35e-4,3.57e-4])*np.array([coe])
        list5=np.array([4.45e-4,4.6e-4,5.2e-4,5.116e-4,5.3e-4])*np.array([coe])
        list6 = np.array([7.4e-4, 7.3e-4, 6.5e-4, 7.35e-4, 4.8e-4]) * np.array([coe])
        list7 = np.array([3.1e-4, 4.3e-4, 4.4e-4, 4.116e-4, 3.3e-4]) * np.array([coe])
        data={
            '1D-LN5':list0,
            'DS-4': list1,
            'DS-5': list2,
            '1D-Alex': list3,
            'DAE':list4,
            'GAM':list5,
            '2D-Alex': list6,
            'DSI': list7
        }
        df=pd.DataFrame(data)
        df.plot.box(title="time of evaluation one compression")
        plt.grid(linestyle="--",alpha=0.4)
        plt.xlabel("Methods")
        plt.ylabel("time (s)")
        plt.show()
if __name__ == '__main__':
    drawpic=DrawResults()
    #drawpic.drawbox() #箱状图
    #drawpic.drawbox2()  #liang大论文箱状图
    drawpic.loadDataFromExcel()
    #drawpic.drawHistoprogrambyMatplot()
    #drawpic.drawHistoprogrambyMatplotFordiffpath()
    drawpic.drawHistoprogrambyMatplotForcmp()
    #drawpic.loadDataFromExcel()  #下面两句用于画预测结果与真实结果
    #drawpic.drawHistoprogrambyMatplot()


