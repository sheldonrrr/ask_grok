#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from setuptools import setup, find_packages

package_name = "Ask AI Plugin"

if sys.version_info < (2, 7):
    sys.exit(package_name + ' requires Python 2.7 or newer.')

setup(
    name=package_name,
    version='1.3.0',
    description='Ask AI about your books',
    author='Sheldon',
    author_email='sheldonrrr@gmail.com',
    packages=['ask_ai_plugin'],
    include_package_data=True,
    platforms=['windows', 'osx', 'linux'],
    install_requires=['requests'],
    zip_safe=False,
    keywords='bookAI readingAI x.AI GrokAI GeminiAI',
    package_data={
        'ask_ai_plugin': ['images/*.png', 'lib/*']
    }
)
