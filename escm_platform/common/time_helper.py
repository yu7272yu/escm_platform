# coding=utf-8
import time
import arrow
import datetime
from datetime import timedelta
from datetime import date


class TimeHelper(object):
    def __init__(self):
        pass

    def get_today(self):
        """
        获取当天日期-字符串
        :return:
        """
        # 获取当天的日期
        today_date = date.today().strftime('%Y%m%d')
        return today_date

    # 获取几天前的日期
    def get_before_today(self, days):
        """
        获取几天前日期字符串--可以是负数
        :param days:
        :return:
        """
        before_date = (date.today() - timedelta(days)).strftime('%Y%m%d')
        return before_date

    def time_int_to_date(self, timestamp):
        if not isinstance(timestamp, int):
            timestamp = int(timestamp)

        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

        return date_time

    def get_weekday(self):
        weekday = arrow.now().weekday()
        print('weekday--{}'.format(weekday))
        return weekday

    def today_time_int(self):
        """
        获取当天的时刻--24小时值 --比如 1747
        :return:
        """
        now = datetime.datetime.now()
        return str(now.strftime("%Y-%m-%d %H%M")).split(' ')[1]


if __name__ == '__main__':
    time_helper = TimeHelper()
    time_helper.get_today()
    data = '20220530'
    before_time = time_helper.get_before_today(-30)
    #
    # if int(before_time) >= int(data):
    #     print('过期')
    # else:
    #     print('没过期')
    int_time = 1655454006

    print(time_helper.time_int_to_date(int_time))