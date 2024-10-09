# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kauldron']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kauldron',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Conchylicultor',
    'author_email': 'etiennefg.pot@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
