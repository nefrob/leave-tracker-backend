# Ref: https://packaging.python.org/tutorials/packaging-projects/
# python3 setup.py develop

from setuptools import setup, find_packages

setup(
    name='backend',
    version='0.1',
    packages=find_packages(),
    description='Tilt Leave Tracker Assignment',
    author='Robert Neff',
    author_email='rneff@cs.stanford.edu',
    url='https://github.com/nefrob/leave-tracker-backend',
    zip_safe = False,
    install_requires=['flask', 'flask_restful', 'flask_sqlalchemy', \
        'flask_marshmallow', 'flask_cors', 'sqlalchemy', 'marshmallow'],
    python_requires='>=3.7'
)