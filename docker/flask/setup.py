from setuptools import setup

setup(
    name='thesr_flask_app',
    packages=['thesr_flask_app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'thesr'
    ],
)
