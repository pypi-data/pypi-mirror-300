# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup

setup(
    name='psx-syntax',
    version='0.0.1',
    url='https://github.com/coryfitz/psx-syntax',
    download_url='https://github.com/coryfitz/psx-syntax',
    license='BSD',
    author='Cory Fitz',
    author_email='',
    description='JSX style syntax for Python',
    long_description=open('README.md').read(),
    zip_safe=False,
    classifiers=[
    ],
    platforms='any',
    py_modules=['psx-syntax'],
    include_package_data=True,
)
