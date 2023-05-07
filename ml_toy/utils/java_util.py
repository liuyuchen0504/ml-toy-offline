# -*- coding:utf-8 -*-
# ====================
# Author liuyuchen
# Date 2023/5/6
# 
# ====================
import json
import jpype
from contextlib import contextmanager

__all__ = ["get_java_class", "get_udf_conf"]


@contextmanager
def get_java_class(clazz, jar_path):
    """获取 java 中的类

    :param clazz:       类名，全称
    :param jar_path:    类所在的 jar 包
    :return: Class
    """
    # 获取jvm.dll 的文件路径
    jvm_path = jpype.getDefaultJVMPath()
    if not jpype.isJVMStarted():
        jpype.startJVM(jvm_path, "-ea", "-Djava.class.path=%s" % (jar_path))
    yield jpype.JClass(clazz)
    jpype.shutdownJVM()


def get_udf_conf(clazz, jar_path):
    with get_java_class(clazz, jar_path) as clazz:
        conf = clazz.getUDFConf()
        return json.loads(str(conf))

