# -*- coding:utf-8 -*-
# ====================
# Author Liu Yuchen
# Date 2023/5/2
#
# 算子和 Java 共享，因此
# 本部分主要是任务是将
# Java 算子注册成 UDF
# ====================
from ml_toy.utils.type_util import to_udf_type


def register_java_udf(spark, name, clazz, return_type):
    """注册 UDF

    :param spark:          PySpark 客户端
    :param name:           方法的名字
    :param clazz:          方法调用的 UDF 类，全名
    :param return_type:    方法返回类型
    """
    spark_version = float(".".join(spark.version.split(".")[:2]))
    # 不同的 spark 版本，注册方式不同
    if spark_version >= 2.3:
        udf_register_func = spark.udf.registerJavaFunction
    elif spark_version >= 2.1:
        from pyspark.sql import SQLContext
        udf_register_func = SQLContext(spark).registerJavaFunction
    else:
        raise ValueError("The pySpark version should >= 2.1")

    if isinstance(return_type, str):
        return_type = to_udf_type(return_type)

    udf_register_func(name, clazz, return_type)


