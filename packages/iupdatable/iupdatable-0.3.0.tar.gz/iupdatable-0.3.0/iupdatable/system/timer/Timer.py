from datetime import datetime
import time
import random
import asyncio
import ast


class Timer(object):

    @staticmethod
    def timestamp() -> int:
        """
        get Unix timestamp(Accurate to the second, 10 digits)
        获取 Unix 时间戳（精确到秒，10位数）
        :return:
        """
        return int(time.time())

    @staticmethod
    def unix() -> int:
        """
        get Unix timestamp(Accurate to the second, 10 digits)
        获取 Unix 时间戳（精确到秒，10位数）
        :return:
        """
        return int(time.time())

    @staticmethod
    def unix10() -> int:
        """
        get Unix timestamp(Accurate to the second, 10 digits)
        获取 Unix 时间戳（精确到秒，10位数）
        :return:
        """
        return int(time.time())

    @staticmethod
    def unix13() -> int:
        """
        get Unix timestamp(Accurate to the second, 13 digits)
        获取 Unix 时间戳（精确到秒，13位数）
        :return:
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def timestamp13() -> int:
        """
        get Unix timestamp(Accurate to the second, 13 digits)
        获取 Unix 时间戳（精确到秒，13位数）
        :return:
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def sleep_range(min_sec: float, max_sec: float):
        """
        Wait a few seconds randomly
        随机等待若干秒
        :param min_sec: Lower limit
        :param max_sec: Upper limit
        :return:
        """
        rand_sec = random.randint(int(min_sec * 1000), int(max_sec * 1000)) / 1000
        time.sleep(rand_sec)

    @staticmethod
    async def sleep_range_async(min_sec: float, max_sec: float):
        """
        Asynchronously wait for a few seconds randomly
        异步随机等待若干秒
        :param min_sec: Lower limit
        :param max_sec: Upper limit
        :return:
        """
        rand_sec = random.randint(int(min_sec * 1000), int(max_sec * 1000)) / 1000
        await asyncio.sleep(rand_sec)

    @staticmethod
    def unix_to_datetime(unix, tz=None):
        """
        Unix timestamp to datetime
        Unix 时间戳 转 datetime
        :param unix: Unix timestamp
        :param tz: 时区 timezone
        :return: 失败返回 None
        """
        if isinstance(unix, str):
            unix = ast.literal_eval(unix.strip())
        if isinstance(unix, float):
            if unix < 0:
                return None
            return datetime.fromtimestamp(unix, tz)
        if isinstance(unix, int):
            if unix < 0:
                return None
            if len(str(unix)) == 10:
                return datetime.fromtimestamp(unix, tz)
            if len(str(unix)) == 13:
                return datetime.fromtimestamp(unix/1000, tz)
            if len(str(unix)) < 13:
                return datetime.fromtimestamp(unix, tz)
            if len(str(unix)) > 13:
                return None
        else:
            return None

    @staticmethod
    def timestamp_to_datetime(unix, tz=None):
        """
        Unix timestamp to datetime
        Unix 时间戳 转 datetime
        :param unix: Unix timestamp
        :param tz: 时区 timezone
        :return: 失败返回 None
        """
        return Timer.unix_to_datetime(unix, tz)

    @staticmethod
    def unix_to_datetime_str(unix, fmt="", tz=None):
        """
        Unix timestamp to datetime string
        Unix 时间戳 转 datetime 字符串
        :param unix: Unix timestamp
        :param fmt: 格式化字符串 format string, default is empty
        :param tz: 时区 timezone
        :return: default output example: 2020-12-25 17:17:42
        """
        dt = Timer.unix_to_datetime(unix, tz)
        if len(fmt.strip()) == 0:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return dt.strftime(fmt)

    @staticmethod
    def timestamp_to_datetime_str(unix, fmt="", tz=None):
        """
        Unix timestamp to datetime string
        Unix 时间戳 转 datetime 字符串
        :param unix: Unix timestamp
        :param fmt: 格式化字符串 format string, default is empty
        :param tz: 时区 timezone
        :return: default output example: 2020-12-25 17:17:42
        """
        return Timer.unix_to_datetime_str(unix, fmt, tz)

    @staticmethod
    def parse_datetime_str(dt_str, fmt="%Y-%m-%d %H:%M:%S"):
        """
        Parse datetime string to datetime
        解析 datetime 字符串为 datetime
        :param dt_str: datetime string
        :param fmt: 格式化字符串 format string, default is "%Y-%m-%d %H:%M:%S"
        :return: 失败返回 None
        """
        try:
            return datetime.strptime(dt_str, fmt)
        except Exception as e:
            return None

    @staticmethod
    def get_formatted_datetime_str(dt=None, fmt="%Y-%m-%d %H:%M:%S"):
        """
        Get formatted datetime string
        获取格式化的 datetime 字符串
        :param dt: datetime object, default is current time
        :param fmt: 格式化字符串 format string, default is "%Y-%m-%d %H:%M:%S"
        :return: 格式化后的 datetime 字符串
        """
        if dt is None:
            dt = datetime.now()
        return dt.strftime(fmt)

    @staticmethod
    def get_formatted_date_str(dt=None, fmt="%Y-%m-%d"):
        """
        Get formatted date string
        获取格式化的 日期 字符串
        :param dt: datetime object, default is current datetime
        :param fmt: 格式化字符串 format string, default is "%Y-%m-%d"
        :return: 格式化后的 日期 字符串
        """
        return Timer.get_formatted_datetime_str(dt, fmt)

    @staticmethod
    def get_formatted_time_str(dt=None, fmt="%H:%M:%S"):
        """
        Get formatted time string
        获取格式化的 时间 字符串
        :param dt: datetime object, default is current datetime
        :param fmt: 格式化字符串 format string, default is "%H:%M:%S"
        :return: 格式化后的 时间 字符串
        """
        return Timer.get_formatted_datetime_str(dt, fmt)

    @staticmethod
    def get_today_str(fmt="%Y-%m-%d"):
        """
        Get today string
        :param fmt: 格式化字符串 format string, default is "%Y-%m-%d"
        :return: 格式化后的 日期 字符串
        """
        return Timer.get_formatted_datetime_str(datetime.now(), fmt)

    @staticmethod
    def get_now_str(fmt="%Y-%m-%d %H:%M:%S"):
        """
        Get now string
        :param fmt: 格式化字符串 format string, default is "%Y-%m-%d %H:%M:%S"
        :return: 格式化后的 日期+时间 字符串
        """
        return Timer.get_formatted_date_str(datetime.now(), fmt)

    @staticmethod
    def get_now_date_str(fmt="%Y-%m-%d"):
        """
        Get now date string
        :param fmt: 格式化字符串 format string, default is "%Y-%m-%d"
        :return: 格式化后的 时间 字符串
        """
        return Timer.get_formatted_datetime_str(datetime.now(), fmt)

    @staticmethod
    def get_now_time_str(fmt="%H:%M:%S"):
        """
        Get now time string
        :param fmt: 格式化字符串 format string, default is "%H:%M:%S"
        :return: 格式化后的 时间 字符串
        """
        return Timer.get_formatted_datetime_str(datetime.now(), fmt)
