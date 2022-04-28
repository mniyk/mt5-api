import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='mt5-api',
    version='0.0.1',
    author='mniyk',
    author_email='my.name.is.yohei.kono@gmail.com',
    description='mt5 api python library',
    long_description=long_description,
    url='https://github.com/mniyk/mt5-api.git',
    packages=setuptools.find_packages(),
    install_requires=['MetaTrader5'])