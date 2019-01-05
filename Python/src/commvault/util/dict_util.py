#!/usr/bin/python
# -*- coding: UTF-8 -*-


def dict_update_child(dictobj, value, children_name, *parents):
    child = dict_get_child(dictobj, parents)
    child[children_name] = value
    return dictobj


def dict_get_child(dictobj, parents=()):
    result = dictobj
    for parent in parents:
        result = result.get(parent)
        if result is None:
            break

    return result


def dict_get_converted_value(dictobj, children_name, func):
    return func(dictobj.get(children_name))


def dict_remove_null_pair(dictobj):
    if not isinstance(dictobj, dict):
        return False

    # 返回布尔值, 是否有删除空值
    result = False
    for key in list(dictobj.keys()):
        value = dictobj.get(key)
        if not value and not isinstance(value, bool):
            del dictobj[key]
            result = True
        elif isinstance(value, list) or isinstance(value, tuple):
            # 清空列表中的多项空值
            new_value = [i for i in value if i is not None and i != "" and i != {} and i != [] and i != () and
                         (not dict_remove_null_pair(i) or i)]
            if new_value:
                dictobj[key] = new_value
            else:
                del dictobj[key]
                result = True
        elif isinstance(value, dict):
            result = dict_remove_null_pair(value)
            if not dictobj.get(key) and not isinstance(dictobj.get(key), bool):
                del dictobj[key]
                result = True

    return result
