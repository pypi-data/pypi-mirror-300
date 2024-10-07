from setuptools import setup, find_packages
import os

VERSION = os.environ['GITHUB_REF_NAME'].removeprefix('v-')
DESCRIPTION = 'lambdarepy description'
LONG_DESCRIPTION = 'lambdarepy long description'

setup(
    name="lambdarepy",
    version=VERSION,
    author="caolan947 (Caolán Daly)",
    author_email="<caolan.day94@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    py_modules=['repy']
)