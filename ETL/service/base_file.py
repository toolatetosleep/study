# encoding: utf-8
"""
日志处理服务基类
@author Yuriseus
@create 2016-8-17 15:02
"""
import time

import settings
from consumer.file import FileConsumer
from db.db_mysql import DBMySQL
from log import logger
from util.parser import ParserUtil


class BaseFileService(FileConsumer):
    def __init__(self, dir_path):
        super().__init__(dir_path)

        self.parser = ParserUtil
        db_conf = settings.CONF['db']
        self.db = DBMySQL(db_conf['host'], db_conf['port'], db_conf['user'], db_conf['password'], db_conf['db'])
        self.log = logger

        self._start_time = 0
        self._check_time = 6    # 秒
        self._tmp_lines = []
        self.batch_lines_count = 10000    # 一次处理行数

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
        if len(self._tmp_lines) < self.batch_lines_count:
            self._tmp_lines.append(line_data)

        if len(self._tmp_lines) >= self.batch_lines_count:
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

    def check_batch_process(self):
        """
        自动按时间窗口检测批处理。解决当数据不足指定行数时不处理的问题
        """
        if time.time() - self._start_time > self._check_time and self._tmp_lines:
            self.process(self._tmp_lines)
            self._tmp_lines = []

    def process(self, lines):
        """
        处理日志数据
        :param lines: 多行内容list
        :return:
        """
        raise NotImplementedError('must implement process')
