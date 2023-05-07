# -*- coding:utf-8 -*-
# ====================
# Author liuyuchen
# Date 2023/5/6
# 
# ====================
from ml_toy.utils.java_util import get_udf_conf


def test_get_udf_conf():
    config = get_udf_conf("cn.lonnrot.feature.operate.udf.UDFConf",
                          "../jars/ml-toy-feature-1.0-SNAPSHOT.jar")
    assert isinstance(config, dict) and len(config) > 0

