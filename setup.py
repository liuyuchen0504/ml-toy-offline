# -*- coding: utf-8 -*-
"""

版本号命名规则：

1.2.0.dev1  # Development release
1.2.0a1     # Alpha Release
1.2.0b1     # Beta Release
1.2.0rc1    # Release Candidate
1.2.0       # Final Release
1.2.0.post1 # Post Release
15.10       # Date based release
23          # Serial release


@Author: Liu Yuchen
"""
import re
from os.path import join
from setuptools import setup, find_packages

MODULE_NAME = "ml_toy"


def get_version():
    VERSION_FILE = join(MODULE_NAME, "__init__.py")
    lines = open(VERSION_FILE, "rt").readlines()
    version_regex = r"^__version__\s*=\s*['\"]([^'\"]*)['\"]"
    for line in lines:
        mo = re.search(version_regex, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError("Unable to find version in %s." % (VERSION_FILE,))


def get_dependencies():
    with open("requirements.txt", "rt") as f:
        lines = filter(lambda x: not (x.startswith("--")
                                      or x.startswith("-")
                                      or x.startswith("#")),
                       map(lambda x: x.strip().strip(" "), f.readlines()))
    return filter(lambda x: x, lines)


setup(name=MODULE_NAME,
      version=get_version(),
      url="https://github.com/Inforg0504/ml-toy-offline.git",
      license="MIT",
      author="Liu Yuchen",
      author_email="liuyuchen54@163.com",
      description="Machine Learning Toy",
      long_description=open("README.md").read(),
      # 需要处理的包目录(通常为包含 __init__.py 的文件夹)
      packages=find_packages(exclude=["tests"]),
      # 不压缩包，而是以目录的形式安装
      zip_safe=False,
      python_requires=">3, <3.8",
      # 需要打包的文件
      package_data={
          "": ["LICENSE", "README.md", "requirements.txt"],
          "ml_toy": []
      },
      # 安装时依赖包
      install_requires=get_dependencies(),
      # 只在执行setup.py时需要的依赖
      setup_requires=[
          "pytest-runner"
      ],
      # 测试依赖的包
      tests_require=[
          "pytest"
      ])
