from setuptools import setup, find_packages

setup(
    name='my_extension_dependency',
    version='0.1.0',
    description='A simple example package',
    author='Erdi Aktan',
    author_email='erdiaktan@gmail.com',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)