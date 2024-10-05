from setuptools import setup, find_packages

setup(
    name='fluent_simple_logger',
    version='0.1.10',
    author='fluentdev',
    author_email='m1@fluent.dev',
    description='A simple logger library for Python.',
    url='https://github.com/m1serybtw/simple_logger',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
