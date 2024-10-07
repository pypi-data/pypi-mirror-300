from setuptools import setup, find_packages

setup(
    name='worldtimebuddy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pytz',
    ],
    entry_points='''
        [console_scripts]
        worldtimebuddy=worldtimebuddy.cli:cli
    ''',
)