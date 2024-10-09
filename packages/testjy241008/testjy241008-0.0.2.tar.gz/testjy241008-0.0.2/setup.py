from setuptools import setup, find_packages

setup(
    name='testjy241008',
    version='0.0.2',
    description='PYPI tutorial package creation written by TeddyNote',
    author='jeeyz',
    author_email='like.g.orwell@gmail.com',
    url='https://github.com/JeeYz/like_g_orwell',
    install_requires=['pytest'],
    packages=find_packages(exclude=[]),
    keywords=[''],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

