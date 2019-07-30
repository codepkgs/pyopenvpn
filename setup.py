from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyopenvpn',
    version='0.0.3',
    keywords='openvpn',
    description='manage openvpn',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='zhanghe',
    author_email='x_hezhang@126.com',
    url='https://github.com/x-hezhang/pyopenvpn',
    license='GPLv3',
    packages=find_packages()
)
