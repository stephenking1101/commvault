#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import xmltodict


def load_json(file_path):
    try:
        # 获取xml文件
        xml_file = open(file_path, 'r')
        # 读取xml文件内容
        xml_str = xml_file.read()
        # 将读取的xml内容转为json
        jsonstring = xmltodict.parse(xml_str)
    finally:
        if xml_file:
            xml_file.close()

    return jsonstring


if __name__ == "__main__":
    jsonstr = load_json("./create_subclient_template.xml")
    # print(jsonstr)
    # 将 Python 对象编码成 JSON 字符串
    print(json.dumps(jsonstr, sort_keys=True, indent=4, separators=(',', ': ')))

    # 读取json文件
    # json.load()函数的使用，将读取json信息
    # file = open('./create_subclient_template.json', 'r')
    # info = json.load(file)
    # print(info.get("none"))
    # 访问字典里的值的时候，如果直接用 [] 访问，在没有找到对应键的情况下会报错，一个更好的替代方案是用内置的 get 方法来取键值，这时候如果不存在也不会报错。
    # if info.get("subClientProperties").get("commonProperties").get("turboNASClient") is not None:
    #     del info.get("subClientProperties").get("commonProperties")["turboNASClient"]
    # else:
    #     print(info.get("subClientProperties").get("commonProperties").get("turboNASClient") )
    # print(info)



