from setuptools import setup, find_packages
import re


def get_long_description():
    with open('README.md') as f:
        return re.sub('!\[(.*?)\]\(docs/(.*?)\)',
                      r'![\1](https://github.com/mara/mara-cron/raw/master/docs/\2)', f.read())


setup(
    name='mara-cron',
    version='0.9.2',

    description='Lets you manage cron jobs via mara',

    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    url='https://github.com/mara/mara-cron',

    install_requires=[
        'mara-app>=2.2.0',
        'mara-page>=1.5.2',
        'python-crontab>=2.5.1',
        'click>=7.1.2',
    ],
    extras_require={
        'test': ['pytest']
    },

    python_requires='>=3.6',

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',
)
