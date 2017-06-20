from setuptools import setup, find_packages
import dyncli


with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dyn-cli',
    version=dyncli.__version__,
    description=dyncli.__doc__.strip(),
    long_description=long_description,
    url='https://github.com/henriquemenezes/dyn-cli',
    author=dyncli.__author__,
    author_email=dyncli.__author_email__,
    license=dyncli.__license__,
    packages=find_packages(exclude=['docs', 'tests']),
    entry_points={
        'console_scripts': [
            'dyn = dyncli.__main__:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ]
)
