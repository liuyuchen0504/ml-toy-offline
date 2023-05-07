# -*- coding:utf-8 -*-
# ====================
# Author liuyuchen
# Date 2023/5/6
# 
# ====================
from pyspark.sql import session
from ml_toy.feature.operator import register_java_udf
from ml_toy.utils.java_util import get_udf_conf

jar_path = "../jars/ml-toy-feature-1.0-SNAPSHOT.jar"

spark = session.SparkSession \
    .builder \
    .master("local") \
    .appName("test") \
    .config("spark.jars", jar_path) \
    .enableHiveSupport() \
    .getOrCreate()


def test_register_java_udf():
    # 1. 读取 UDF 注册信息
    config = get_udf_conf("cn.lonnrot.feature.operate.udf.UDFConf", jar_path)
    # 2. 注册
    for k, f in config.items():
        register_java_udf(spark, k, f["class"], f["returnType"])

    df = spark.createDataFrame([
        (1, 144, 5, 33, 1),
        (2, 167, 5, 45, 2),
        (3, 124, 5, 23, 1),
        (4, 144, 5, 33, 5),
        (5, 133, 5, 54, 1),
    ], ["id", "weight", "height", "age", "loc"])

    df.registerTempTable("tmp_table")

    # 3. 使用 UDF 函数
    new_df = spark.sql("""
    select 
        weight, height
        , add(cast(weight as int), cast(height as int)) as add_col
        , multiplyInt(weight, height) as mul_col
    from tmp_table
    """)
    print(new_df.show())
    print(df.selectExpr("add(cast(weight as int), cast(height as int)) as add_col").show())
