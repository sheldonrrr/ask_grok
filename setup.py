#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

package_name = "Ask Grok"

if sys.version_info < (2, 7):
    sys.exit(package_name + ' requires Python 2.7 or newer.')

setup(
    name=package_name,
    version='1.1.19',
    description='使用 X.AI Grok 询问关于当前书籍的问题',
    author='Sheldon',
    author_email='boy.liushaopeng@gmail.com',
    packages=['ask_grok'],
    include_package_data=True,
    platforms=['windows', 'osx', 'linux'],
    install_requires=[],
    zip_safe=False,
    keywords='bookAI readingAI grokbook ebook epub',
    package_data={
        'ask_grok': ['images/*.png', 'lib/*']
    }
)
