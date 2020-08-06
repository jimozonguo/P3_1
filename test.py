#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest

if __name__ == '__main__':
    #搜索当前目录中scripts目录中所有以test开头的的py文件(即测试用例脚本)_，然后把这些测试类中的所有以test开头的测试方法都添加测试套件中
    suite=unittest.defaultTestLoader.discover("./scripts/","test*.py");
    #运行该测试套件
    unittest.TextTestRunner().run(suite);