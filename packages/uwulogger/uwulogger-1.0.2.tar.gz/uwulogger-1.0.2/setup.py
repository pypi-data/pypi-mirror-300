
from setuptools import setup, find_packages

setup(
    name='uwulogger',  
    version='1.0.2',
    author='Aizer',
    author_email='mohit.4sure@gmail.com',
    description='A Python logger module for logging in tools',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['python', 'pylogger', 'logger', 'logging', 'aizer logger','tool logger'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.10',  
    install_requires=['colorama']
)
