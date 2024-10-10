from setuptools import setup, find_packages

setup(
    name="gela",  
    version="0.1",  
    description="A Python module that provides a Base class for value management.",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",
    url="",  
    author="Your Name",
    author_email="davitidatunashvili98@gmail.com",
    license="MIT",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  
    python_requires='>=3.6',  
)
