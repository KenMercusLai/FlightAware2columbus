# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flightaware2columbus', 'flightaware2columbus.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'requests-html>=0.10.0,<0.11.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'flightaware2columbus',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Ken M. Lai',
    'author_email': 'ken.mercus.lai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
