from setuptools import setup, find_packages

setup(
    name="simplecmdinterface",  
    version="0.3.0",
    author="Ioannis Tsampras",
    author_email="ioannis.tsampras@ac.upatras.gr",
    description="A simple windows command line interface wrapper for use with cli's",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Skorpinakos/Simple-CMD-Interface-for-Python",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
         "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.8',
)
