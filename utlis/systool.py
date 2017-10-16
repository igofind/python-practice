# encoding=utf-8
import os
import platform
import sys
import time


def version():
    version_ = '%d.%d' % sys.version_info[:2]
    return float(version_)


def is_python3():
    return version() >= 3


# 生成13位的时间戳
def timestamp():
    return int(time.time() * 1000)


def get_platform():
    return platform.system()


def is_windows():
    return get_platform() == "Windows"


def is_linux():
    return get_platform() == "Linux"


def is_mac():
    return get_platform() == "Darwin"


# 保持控制台不退出
def pause():
    if is_windows():
        os.system('pause')
    else:
        os.system('echo "按任意键继续..." && read')
