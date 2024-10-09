import setuptools
from setuptools import find_packages

setuptools.setup(name='ankerautotrainsdk',
                 version="0.9",
                 description='Python Package Boilerplate',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type="text/markdown",
                 author='taco',
                 author_email='taco.wang@anker-in.com',
                 url='',
                 # py_modules=['sdk'],
                 install_requires=["requests", "pydantic"],
                 license='MIT License',
                 zip_safe=False,
                 keywords='',
                 packages=find_packages()
)