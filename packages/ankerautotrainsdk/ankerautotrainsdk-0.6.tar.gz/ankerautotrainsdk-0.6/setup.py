import setuptools
from setuptools import find_packages

setuptools.setup(name='ankerautotrainsdk',
                 version="0.6",
                 description='Python Package Boilerplate',
                 long_description=open('README.md').read().strip(),
                 author='taco',
                 author_email='taco.wang@anker-in.com',
                 url='',
                 # py_modules=['sdk'],
                 install_requires=["requests"],
                 license='MIT License',
                 zip_safe=False,
                 keywords='',
                 packages=find_packages()
)