#!/usr/bin/env python3

def open_file(filename, mode='rt'):
    if filename == '-':  # '-' 表示从标准输入读取
        import sys
        if 'b' in mode:  # 二进制模式
            return sys.stdin.buffer
        else:  # 文本模式
            return sys.stdin
    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode)
    elif filename.endswith('.bz2'):
        import bz2
        return bz2.open(filename, mode)
    elif filename.endswith('.zip'):
        import zipfile
        zfile = zipfile.ZipFile(filename)
        name = zfile.namelist()[0]  # 获取第一个文件的名称
        return zfile.open(name, mode='r')
    else:
        return open(filename, mode)


def open_file_process(filename, process_func, mode='rt', *args, **kwargs):
    if filename.endswith('.gz'):
        import gzip
        with gzip.open(filename, mode) as file:
            for line in file:
                process_func(line, *args, **kwargs)
    elif filename.endswith('.bz2'):
        import bz2
        with bz2.open(filename, mode) as file:
            for line in file:
                process_func(line, *args, **kwargs)
    elif filename.endswith('.zip'):
        import zipfile
        with zipfile.ZipFile(filename) as zfile:
            for name in zfile.namelist():
                with zfile.open(name, mode='r') as file:
                    for line in file:
                        process_func(line.decode('utf-8'), *args, **kwargs)
    else:
        with open(filename, mode) as file:
            for line in file:
                process_func(line, *args, **kwargs)
