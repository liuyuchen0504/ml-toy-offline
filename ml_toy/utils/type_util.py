# -*- coding:utf-8 -*-
# ====================
# Author liuyuchen
# Date 2023/5/6
# 
# ====================
import re
from pyspark.sql.types import *


def to_udf_type(tpe: str):
    """python type or java type trans pyspark type

    :param tpe: str. python type
    :return:    pyspark type
    """
    tpe = _type_trans(tpe)
    if tpe in ["short"]:
        return ShortType()
    elif tpe in ["int", "integer"]:
        return IntegerType()
    elif tpe in ["long", "bigint"]:
        return LongType()
    elif tpe == "float":
        return FloatType()
    elif tpe == "double":
        return DoubleType()
    elif tpe == "decimal":
        return DecimalType()
    elif tpe in ["string", "str"]:
        return StringType()
    elif tpe in ["bool", "boolean"]:
        return BooleanType()
    else:
        _LIST = r"(\w+)<(\w+)>"
        _MAP = r"map<(\w+),(\w+)>"
        map_type = re.match(_MAP, tpe)
        if map_type:
            key_type = map_type.group(2).split(".")[-1]
            value_type = map_type.group(3).split(".")[-1]
            return MapType(to_udf_type(key_type), to_udf_type(value_type))
        list_type = re.match(_LIST, tpe)
        if list_type:
            assert list_type.group(1) in ["list", "array"]
            ele_type = list_type.group(2)
            return ArrayType(to_udf_type(ele_type))
        raise ValueError("The type[%s] is not supported." % tpe)


def _type_trans(tpe: str) -> str:
    """对 type 做一次转换

    :param tpe: str
    :return:    str
    """
    _LIST = r"([\w\.]*)<([\w\.]*)>"
    _MAP = r"([\w\.]*)Map<([\w\.]*),([\w\.]*)>"

    tpe = tpe.lower()
    map_type = re.match(_MAP, tpe)
    if map_type:
        key_type = map_type.group(2).split(".")[-1]
        value_type = map_type.group(3).split(".")[-1]
        return "map<{key},{value}>".format(key=key_type, value=value_type)
    list_type = re.match(_LIST, tpe)
    if list_type:
        col_tpe = list_type.group(1).split(".")[-1]
        ele_tpe = list_type.group(2).split(".")[-1]
        return "{col_tpe}<{ele_tpe}>".format(col_tpe=col_tpe, ele_tpe=ele_tpe)
    else:
        return tpe.split(".")[-1]

