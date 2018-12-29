#!/usr/bin/python
# coding=utf-8

# -*- coding: utf-8 -*-
import argparse
from commvault.api import API
from commvault.rest_api_json import RestAPI
from commvault.logger import logger
from commvault.util import dict_util
from openpyxl import load_workbook
import os
import yaml
import json


class Commander:

    def __init__(self, system_config="./system_config.yaml"):
        self.logger = logger.getlogger(Commander.__name__)
        self.logger.debug("Init application with config file: %s", system_config)
        self.system_properties = {}
        if os.path.exists(system_config):
            with open(system_config, "r") as f:
                self.system_properties = yaml.safe_load(f.read())
        # print(self.system_properties.get("setup").get("field_mapping"))

        self.conf_array = []
        self.logger.debug("Inited application with configs: %s", self.system_properties)

    def create_nas_subclient(self, api=API()):
        src_path = os.path.dirname(os.path.realpath(__file__))
        # cwd = os.getcwd() # current working directory

        api.login(self.system_properties.get("server"))
        template_path = src_path + "/commvault/template/create_subclient_template.json"
        template = {}
        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                template = json.load(f)
        self.logger.debug("Create NAS subclient with template: %s", template)

        storage_policy_name_list, policies = api.get_storage_policy()
        storage_policy_name_list.sort(reverse=True)

        for conf in self.conf_array:
            self.logger.debug("Creating subclient in client: %s", conf.get(self.get_field_mapping_val("clientname")))

            osname = conf.get(self.get_field_mapping_val("os")).strip()
            important_system_flag = conf.get(self.get_field_mapping_val("important_system_flag")).strip()
            important_data_flag = conf.get(self.get_field_mapping_val("important_data_flag")).strip()
            datatype = conf.get(self.get_field_mapping_val("datatype")).strip()
            clientname = conf.get(self.get_field_mapping_val("clientname")).strip()
            appname = ""
            if osname.lower() == "nas":
                appname = "NAS"

            if important_system_flag == u"否" or important_data_flag == u"否":
                storage_policy_name = "L34_"
            else:
                storage_policy_name = "L12_"

            if datatype == u"应用日志":
                storage_policy_name = storage_policy_name + "APPLOG"

            for sp in storage_policy_name_list:
                if sp.startswith(storage_policy_name):
                    storage_policy_name = sp
                    break

            subclient_list, subclient_properties = api.get_subclient(client_name=clientname)
            subclient_name = storage_policy_name
            while subclient_name in subclient_list:
                self.logger.debug("Subclient %s already exists", subclient_name)
                seq = subclient_name[subclient_name.rindex("_") + 1:]
                subclient_name = subclient_name[:subclient_name.rindex("_") + 1] + str(int(seq) + 1)

            api.create_subclient(appname=appname,
                                 clientname=clientname,
                                 subclientname=subclient_name,
                                 storage_policy_name=storage_policy_name,
                                 paths=[conf.get(self.get_field_mapping_val("path")).strip()],
                                 descpt=conf.get(self.get_field_mapping_val("description")).strip(),
                                 content_operation_type="ADD",
                                 template=template)

        api.logout()

    def get_field_mapping_val(self, key):
        mapping = dict_util.get_dict_child(self.system_properties, ("setup", "field_mapping"))
        return mapping.get(key)

    def load_excel(self, filename):
        self.logger.debug("Going to load excel file: %s", filename)
        # 打开一个workbook
        wb = load_workbook(filename, read_only=True)

        # 获取所有表格(worksheet)的名字
        sheets = wb.sheetnames

        # 第一个表格的名称
        sheet_first = sheets[0]

        # 获取特定的worksheet
        ws = wb[sheet_first]

        # 获取表格所有行和列，两者都是可迭代的
        rows = ws.rows

        col_title = []
        # 迭代所有的行
        for i, row in enumerate(rows):
            conf = {}
            for j, col in enumerate(row):
                if i == 0:
                    if j == 0 and col.value is None:
                        raise RuntimeError("无法读取数据，首行必须为标题行")
                    else:
                        col_title.append(col.value)
                else:
                    conf[col_title[j]] = col.value

            if len(conf) > 0:
                self.conf_array.append(conf)

        self.logger.debug("Loaded excel data: %s", self.conf_array)
        return self.conf_array


def main():
    applogger = logger.getlogger(__name__)
    src_path = os.path.dirname(os.path.realpath(__file__))
    com = Commander(system_config=src_path+"/system_config.yaml")

    # create top-level parser
    parser = argparse.ArgumentParser()

    # 定位参数的使用, python cli_fw.py 8
    parser.add_argument("userName", help="user to login the CommServe", type=str)
    parser.add_argument("password", help="password of the specific user", type=str)

    subparsers = parser.add_subparsers(help="batchJob -h to show help")

    # create the parser for the 'batchJob' command
    parser_create_subclient = subparsers.add_parser('batchJob', help='Bulk client/subclient creation and configuration')
    parser_create_subclient.set_defaults(func=com.create_nas_subclient)
    parser_create_subclient.add_argument('filepath', type=str,
                                         help='Excel file path that contains subclient config')

    args = parser.parse_args()
    applogger.debug("arguments: %s", args)
    # for test
    # parser.parse_args(['--help'])
    # parser.parse_args(['createSubclient', '-h'])
    # args = parser.parse_args("server user pwd createSubclient app client subclient".split())

    api = RestAPI(args.userName, args.password)
    com.load_excel(args.filepath)
    # call sub command
    args.func(api)


if __name__ == "__main__":
    main()
