# CPHOS_ToolKit
A Toolkit for CPHOS affairs, including managing database, data analysis, ...

该readme文档包含：

1. 对该repo的大体介绍
2. 本repo的依赖包安装与使用方法
3. `/api`目录下各api的接收参数、返回参数（这一部分被移到了群文档“toolkit_1_api”中
4. ...



## 1、整体介绍

本repo以python为胶水语言，通过远程操控CPHOS数据库的方式，实现了对CPHOS后台阅卷系统的数据库的设置与调整。

其中，所有使用mysql语言对数据库进行增删改查操作的、以及登录、开启事务与提交事务的，都由api中的文件实现。为了实现高级功能，仅需调用api即可。

本repo的结构如下。（待完善）

```
-api
 |_ apis to the dataset
-other dirs

readme.md

    
```

## 2、本repo的依赖安装与使用方法

首先安装python。
随后，在本repo根目录下执行：
```bash
pip install -r requirements.txt
```
即可完成依赖。
之后，在根目录运行：
```bash
python test.py
```
即可。如果您是linux平台，应该为：
```bash
python3 test.py
```
