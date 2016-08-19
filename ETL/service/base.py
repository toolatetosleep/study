# encoding: utf-8
"""
日志处理服务基类
@author Yuriseus
@create 2016-8-17 15:02
"""
import time
from consumer.base import Consumer
from db.db_sqlalchemy import SQLAlchemy
from util.parser import ParserUtil
from log import logger


class BaseService(Consumer):
    def __init__(self, topics, group_id=None, bootstrap_servers=None):
        if not group_id:
            group_id = 'python-etl-group'
        if not bootstrap_servers:
            bootstrap_servers = ['192.168.1.102:9092']
        super().__init__(topics, group_id, bootstrap_servers)

        self.parser = ParserUtil
        self.db = SQLAlchemy.instance()
        self.log = logger

        self._start_time = 0
        self._check_time = 60    # 秒
        self._tmp_lines = []
        self._lines_len = 1    # 一次处理行数

    def consume(self, line_data):
        """
        消费一行数据
        :param line_data:
        :return:
        """
        if self.is_need_drop(line_data):
            return
        line_data = self.get_clean_data(line_data)
        self._start_time = time.time()
        if len(self._tmp_lines) < self._lines_len:
            self._tmp_lines.append(line_data)

        if len(self._tmp_lines) >= self._lines_len:
            self.process(self._tmp_lines)
            self._tmp_lines = []

    def is_need_drop(self, line_data):
        """
        是否需要丢弃该行数据
        :param line_data:
        :return:
        """
        return False

    def get_clean_data(self, line_data):
        """
        获取清洗过的行数据。清洗过程：转换、补全数据
        :param line_data:
        :return:
        """
        return line_data

    def check_process(self):
        """
        自动按时间窗口检测处理。解决当数据不足指定行数时不处理的问题
        """
        if time.time() - self._start_time > self._check_time:
            self.process(self._tmp_lines)
            self._tmp_lines = []

    def process(self, lines):
        """
        处理日志数据
        :param lines: 多行内容list
        :return:
        """
        raise NotImplementedError('must implement process')

    def start(self):
        self.handle()

    def stop(self):
        self.close()
