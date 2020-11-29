#!/bin/bash
echo OFF

echo .:::::::::::::::::::::::::::::::::::::::::::::::::

echo .::

echo .::                 接口测试

echo .::

echo .::               作者： CMQ


echo .:::::::::::::::::::::::::::::::::::::::::::::::::

echo .[ INFO ] 运行环境准备

# 从配置文件中安装环境依赖库i
if [ -f requirements.txt ];
then
     pip install -r requirements.txt
fi
if [ ! -f requirements.txt ];
then
    echo requirements.txt does not exist
fi

echo .[INFO] 运行脚本
python run.py pe cdn