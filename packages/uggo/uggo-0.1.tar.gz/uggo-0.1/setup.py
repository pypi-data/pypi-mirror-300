from setuptools import setup, find_packages

setup(
    name="uggo",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pillow>=10.4.0',
    ],
    author="Matt Wiese",
    author_email="uggo@mattwie.se",
    description="Tastefully ugly charts in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/matthewwiese/uggo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
