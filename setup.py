from setuptools import find_packages, setup

setup(
    name='flasksite',
    version='0.5.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-admin',
        'flask-sqlalchemy',
        'flask-login'
    ],
)
