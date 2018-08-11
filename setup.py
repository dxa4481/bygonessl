from setuptools import setup, find_packages

setup(
    name='bygonessl',
    version='0.0.1',
    description='A tool to descover bygonessl vulnerabilities',
    url='https://github.com/dxa4481/bygonessl',
    author='Dylan Ayrey',
    author_email='dxa4481@rit.edu',
    license='GNU',
    packages = ['bygonessl'],
    install_requires=[
        'pytz==2018.5',
        'python-dateutil==2.7.3',
        'requests==2.19.1'
    ],
    entry_points = {
      'console_scripts': ['bygonessl = bygonessl.bygonessl:main'],
    },
)
