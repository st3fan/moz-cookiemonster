#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from setuptools import setup

install_requires = [
    'Flask==0.10.1',
    'requests==2.3.0'
]

setup(name="moz-cookiemonster",
      version="0.1",
      description="Cookiemonster",
      url="https://github.com/st3fan/moz-cookiemonster",
      author="Stefan Arentz",
      author_email="sarentz@mozilla.com",
      install_requires = install_requires,
      packages=["cookiemonster", "cookiemonster.frontend", "cookiemonster.frontend.static", "cookiemonster.frontend.templates"],
      include_package_data=True,
      scripts=["scripts/cookiemonster-web"])
