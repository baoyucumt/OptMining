''' @File :class_set.py
    @Author:zhangyu,lizhongtian,baoyu
    @Date :2021/7/1 19:19
    @Desc : '''
import datetime
day_dict = {  #330
    1:28,
    2:26,
    3:28,
    4:27,
    5:28,
    6:27,
    7:28,
    8:28,
    9:27,
    10:28,
    11:27,
    12:28
}


def get_time(now_time,days):
    year = now_time.year
    month = now_time.month
    day = now_time.day

    for key in day_dict:
        if key == now_time.month:
            a = day_dict[key]-now_time.day
            if a>=days:
                return datetime.datetime(year,month,day+days)
            else:
                while days != 0:
                    days -= a
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
                    a = day_dict[month]
                    if a >= days:
                        return datetime.datetime(year, month, days)


def sub_time(now_time,days):
    year = now_time.year
    month = now_time.month
    day = now_time.day
    a=days
    while a > 0:
        if a-day<=0:
            return datetime.datetime(year, month, day-a+1)
        a-=day
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        day = day_dict[month]


def sub_time_todays(time1,time2):  #两个日期相减,有点误差,只计算大于的天数
    year1 = time1.year
    month1 = time1.month
    day1 = time1.day
    year2 = time2.year
    month2 = time2.month
    day2 = time2.day
    days=0
    if year1>=year2:
        if month1>=month2:
            for i in range(month2,month1):
                days+=day_dict[i]
            days+=(day1-day2)
            days = days + (year1 - year2) * 330
        else:
            for i in range(month2,13):
                days+=day_dict[i]
            for i in range(1,month1):
                days+=day_dict[i]
            days+=(day1-day2)
            days=days+(year1-year2-1)*330
    else:
        days=-10
    return days



if __name__ == "__main__":
    year = 2021
    month = 4
    day = 21
    days =94
    now_time = datetime.datetime(year,month,day)
    print(get_time(now_time,days))