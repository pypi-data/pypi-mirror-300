#!/usr/bin/env python
# coding=utf-8
'''
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 16:09:20
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-10-06 18:24:57
FilePath: \\Python\\My_Funcs\\OAFuncs\\OAFuncs\\__init__.py
Description:  
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
'''

my_libs = ['oa_cmap', 'oa_data', 'oa_draw', 'oa_file', 'oa_nc']

for lib in my_libs:
    exec(f'from .{lib} import *')