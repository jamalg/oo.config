# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['oo', 'oo.config']

package_data = \
{'': ['*'], 'oo.config': ['test/*']}

setup_kwargs = {
    'name': 'oo.config',
    'version': '0.1.0',
    'description': 'Helpers for environment variable config',
    'long_description': '# oo.config\nHelpers for environment variable config !\n\n*Go to [root directory](https://github.com/jamalg/oo) for other OO packages*',
    'author': 'Jamal Gourinda',
    'author_email': 'jamal.gourinda.pro@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
