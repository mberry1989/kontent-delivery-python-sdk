from setuptools import setup, find_packages

VERSION = "0.0.1" 
DESCRIPTION = "Kentico Kontent Delivery API SDK"


setup(
        name="kontent_delivery",
        version=0.0.1,
        author="Michael Berry",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "astroid==2.5.1",
            "atomicwrites==1.4.0",
            "attrs==20.3.0",
            "beautifulsoup4==4.9.3",
            "certifi==2020.12.5",
            "chardet==4.0.0",
            "colorama==0.4.4",
            "idna==2.10",
            "iniconfig==1.1.1",
            "isort==5.7.0",
            "lazy-object-proxy==1.5.2",
           "mccabe==0.6.1",
           "packaging==20.9",
            "pluggy==0.13.1",
            "py==1.10.0",
            "pylint==2.7.2",
            "pyparsing==2.4.7",
            "pytest==6.2.2",
           "requests==2.25.1",
            "soupsieve==2.2",
            "toml==0.10.2",
            "urllib3==1.26.3",
            "wrapt==1.12.1"
        ],
        keywords=[
            "Kontent",
            "Kontent SDK",
            "Kontent API",
            "Kentico",
            "Kentico API",
            "Kentico Python",
            "Kentico SDK",
            "Kentico Kontent",
            "Kentico Kontent SDK",
            "Kentico Kontent Delivery",
            "Kentico Kontent Delivery SDK",
            "Kentico Delivery",
            "Kentico Delivery SDK",
            ],
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)