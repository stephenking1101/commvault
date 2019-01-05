#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 抽象类加抽象方法就等于面向对象编程中的接口
# from abc import ABCMeta, abstractmethod


class API(object):
    # __metaclass__ = ABCMeta

    def __init__(self, username="admin", password="admin"):
        self.userName = username
        self.password = password

    # @abstractmethod
    def login(self, server, port=81):
        pass

    def logout(self):
        pass

    # @abstractmethod
    def get_storage_policy(self):
        pass

    # @abstractmethod
    def get_schedule_policy(self):
        pass

    # @abstractmethod
    def get_subclient(self, client_id, client_name):
        pass

    # @abstractmethod
    def create_subclient(self, template, appname, clientname, subclientname, storage_policy_name, paths,
                        num_of_backup_streams, backupset_name, descpt,
                        content_operation_type, enable_backup):
        pass

    # @abstractmethod
    def post_execute_qcommand(self, template, command):
        pass
