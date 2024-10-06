from setuptools import setup, find_packages

setup(
    name='psx-syntax',
    version='0.0.2',
    url='https://github.com/coryfitz/psx-syntax',
    download_url='https://github.com/coryfitz/psx-syntax',
    license='BSD',
    author='Cory Fitz',
    author_email='',
    description='JSX style syntax for Python',
    long_description=open('README.md').read(),
    zip_safe=False,
    classifiers=[],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
)
