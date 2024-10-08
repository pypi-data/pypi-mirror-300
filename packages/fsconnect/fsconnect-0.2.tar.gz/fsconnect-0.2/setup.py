# setup.py
from setuptools import setup, find_packages

setup(
    name='fsconnect',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-RESTful',
    ],
    entry_points={
        'console_scripts': [
            'fsconnect=api:app.run',  # This will run the Flask app
        ],
    },
)
