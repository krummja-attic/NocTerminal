from setuptools import find_packages, setup
import sys

install_requires = ['morphism']
if sys.version_info < (3, 5):
    install_requires.append('typing')


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='nocterminal',
    version='0.0.1',
    author='Jonathan Crum',
    author_email="crumja4@gmail.com",
    url="https://github.com/krummja/NocTerminal",
    license='MIT',
    description='BaseTerminal and utilities for roguelike games.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['nocterminal', 'nocterminal.blt', 'nocterminal.ui']),
    install_requires=install_requires,
    setup_requires=[],
    tests_require=['pytest==6.2.1'],
    test_suite='tests',
    python_requires='>=3.8.5',
    )
