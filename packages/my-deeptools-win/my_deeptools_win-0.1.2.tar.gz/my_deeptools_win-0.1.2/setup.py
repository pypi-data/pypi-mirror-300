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
    'version': '0.1.2',
    'description': 'deeptools on windows',
    'long_description': '## *deeptools in wondows*\n\nbased on bamnostic and pybigtools\n-->\n## :writing_hand: xpf\n\n[![pipy](https://img.shields.io/badge/PIPY-0.1.1-green)](https://pypi.org/project/my-deeptools-win/)\n[![github](https://img.shields.io/badge/GITHUB-0.1.1-green)](https://github.com/yang)\n[![windows](https://img.shields.io/badge/WINDOWS-11-blue)](https://www.microsoft.com/zh-cn/windows/windows-11)\n[![bamnostic](https://img.shields.io/badge/BAMNOSTIC-1.0.0-blue)](https://pypi.org/project/bamnostic/)',
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
