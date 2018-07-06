#!/usr/bin/env python
try:    
    from setuptools import setup, find_packages
except:    
    from distutils.core import setup, find_packages
 
setup(name='flask_mongo_session',
      version='1.0.0',
      description='Use mongo db as session.',
      author='Sparrow Jang',
      author_email='sparrow.jang@gmail.com',
      url='https://github.com/eHanlin/flask-mongo-session',
      packages=find_packages(),
      install_requires=['pymongo']
     )   

