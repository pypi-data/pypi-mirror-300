# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_deeptools_win']

package_data = \
{'': ['*']}

install_requires = \
['bamnostic>=1.1.10,<2.0.0',
 'fire>=0.6.0,<0.7.0',
 'matplotlib>=3.9.2,<4.0.0',
 'rich>=13.9.2,<14.0.0']

entry_points = \
{'console_scripts': ['deeptools_win = my_deeptools_win._cli:main']}

setup_kwargs = {
    'name': 'my-deeptools-win',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'xpf10',
    'author_email': '2018303010006@whu.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
