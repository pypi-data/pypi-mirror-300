from setuptools import setup, find_packages

setup(
    name='artksii',
    version='1.0',
    author='Joel Crasta',
    author_email='loejstarc@gmail.com',
    url='https://github.com/joelvcrasta/ascii',
    description='artskii is CLI tool to convert images and videos to ASCII art.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            'artskii = artksii.main:main'
        ],
    },
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',  # Specify your license
    'Operating System :: OS Independent',
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers ',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Utilities',
    ],
)