import os
import re

from setuptools import setup, find_packages


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'yottos_shopify', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in yottos_shopify/__init__.py'
            raise RuntimeError(msg)


install_requires = [
    'Django',
    'mysqlclient',
    'pyactiveresource',
    'ShopifyAPI',
    'django-mysql'
]

setup(
    name="Yottos-Shopify-App",
    version=read_version(),
    url="",
    packages=find_packages(),
    package_data={

    },
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'manage = manage:main',
        ],
    }
)
