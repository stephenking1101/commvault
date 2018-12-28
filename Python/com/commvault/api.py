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
    def createsubclient(self, template, appname, clientname, subclientname, storage_policy_name, paths,
                        num_of_backup_streams="1", backupset_name="defaultBackupSet", descpt="",
                        content_operation_type="", enable_backup="true"):
        pass
