#!/usr/bin/python3
# copyright 2024 CHUA某人

# finds ——在电脑浩如烟海的文件中寻找你想要的文件。
# 用法：import finds;finds.find('文件名', copy=False, open=True)，其中copy参数为True则复制文件路径，opening参数为True则打开文件

import os
import string
import easygui
import platform
import pyperclip


def find(filename, copy=False, opening=False):
    """
    这是函数的主要部分。
    """
    def find_file_on_drive(drive, file_name):
        """
        这个子函数用于寻找给定盘符的程序。
        """
        for foldername, _, filenames in os.walk(drive):
            if filename in filenames:
                return os.path.join(foldername, file_name)

    def search_file_on_all_drives(file_name):
        """
        这个子函数用于寻找本机可用盘符。
        """
        drives = [f'{letter}:' for letter in string.ascii_uppercase if os.path.exists(f'{letter}:')]
        for drive in drives:
            filepath = find_file_on_drive(drive, file_name)
            if filepath:
                return filepath

    file_path = str(search_file_on_all_drives(filename))
    if file_path and copy is True:
        pyperclip.copy(file_path)
        easygui.msgbox(title='Python全盘找文件', msg=f'找到文件{file_path},文件路径已复制到剪切板!')
    elif file_path and opening is True:
        if platform.system() == 'Windows':
            """
            Windows系统下打开文件夹窗口
            """
            os.system(f'explorer {file_path}')
        elif platform.system() == 'Darwin':
            """
            MacOS系统下打开文件夹窗口
            """
            os.system(f'open {file_path}')
        elif platform.system() == 'Linux':
            """
            Linux系统下打开文件夹窗口
            """
            os.system(f'nautilus {file_path}')
        else:
            """
            无法识别的系统
            """
            easygui.msgbox(title='Python全盘找文件', msg=f'无法识别系统，文件为{file_path}！')
    elif file_path:
        easygui.msgbox(title='Python全盘找文件', msg=f'找到文件{file_path}!')
    else:
        easygui.msgbox(title='未找到文件', msg='未找到文件')
