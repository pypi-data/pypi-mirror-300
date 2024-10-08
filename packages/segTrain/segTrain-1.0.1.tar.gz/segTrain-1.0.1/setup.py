#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mzd
# Mail: 1282032474@qq.com
# Created Time:  2024-10-8
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "segTrain",      #这里是pip项目发布的名称
    version = "1.0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "segTrain"),
    description = "llm finetune",

    author = "mzd",
    author_email = "1282032474@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []          #这个项目需要的第三方库
)