# -*- coding:utf8 -*-


import os
import shutil


def copy_files(source_path, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if os.path.exists(source_path):
        # root 所指的是当前正在遍历的这个文件夹的本身的地址
        # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
        # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)
                # print(src_file)

    print('copy files finished!')


def copy_file(file_path, target_path):
    if os.path.exists(file_path):
        shutil.copy(file_path, target_path)
        print(file_path, target_path)


if __name__ == '__main__':
    html_report_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) + "/report/html"
    print(html_report_path)
    copy_file(html_report_path + '/history/history.json', html_report_path + '/widgets')
