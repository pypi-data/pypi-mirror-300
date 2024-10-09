# coding: utf-8
from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='dgtest',  # 包名
      version='1.0.2',  # 版本号
      description='大刚测试开发实战项目',
      long_description=long_description,  # 首页会显示README的说明信息
      author='大刚',
      author_email='152xxxx2668@163.com',
      url='https://github.com/xxxx',
      install_requires=[],  # 存放依赖库，并指明依赖版本
      license='MIT License',  # 许可信息
      packages=find_packages(),  # 要发布的包，多个包可以使用[a,b,c]定义指定包，不指定默认所有
      platforms=["all"],  # 平台
      entry_points={
          'console_scripts': [
              'dgtest = dgtest.main:main'
          ]
      },
      classifiers=[  # 允许包在哪个Python版本下运行
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )
