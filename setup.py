from setuptools import find_packages
from setuptools import setup


try:
    README = open('README.rst').read()
except IOError:
    README = None

setup(
    name='guillotina_chat',
    version="1.0.0",
    description='guillotina_chat',
    long_description=README,
    install_requires=[
        'guillotina'
    ],
    author='guillotina_chat',
    author_email='',
    url='',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    tests_require=[
        'pytest',
    ],
    extras_require={
        'test': [
            'pytest'
        ]
    },
    classifiers=[],
    entry_points={
    }
)
