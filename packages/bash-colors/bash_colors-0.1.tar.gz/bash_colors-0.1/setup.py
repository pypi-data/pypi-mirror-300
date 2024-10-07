from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'Easy tool to add colors to your terminal app!'

# Setting up
setup(
    name="bash-colors",
    version=VERSION,
    author="ilpy",
    author_email="<ilpy@proton.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[]
)