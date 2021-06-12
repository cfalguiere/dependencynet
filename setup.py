from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='dependencynet',
    packages=find_packages(include=['dependencynet',
                                    'dependencynet.network',
                                    'dependencynet.datasource',
                                    'dependencynet.datasource.core']),
    #version='0.2.1-SNAPSHOT',
    version='0.2.1',
    description='This module wraps some data and graph manipulation tools to help analyzing and building representations of directed graphs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Claude Falguiere',
    author_email='',
    license='MIT',
    url='https://github.com/cfalguiere/dependencynet',
    platforms=['Any'],
    install_requires=['pandas', 'networkx', 'ipycytoscape', 'pyyed'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    python_requires='>=3.7',
)
