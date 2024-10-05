from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="beamdust-sdk", 
    version="1.0.1",
    author="Lautaro Torchia",
    author_email="ltorchia@novakorp.io",
    description="A Python SDK for interacting with Beamdust API",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    url="https://github.com/Beamdust/beamdust-package",  
    project_urls={ 
        "Bug Tracker": "https://github.com/Beamdust/beamdust-package/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},  
    packages=find_packages(where="."),  
    python_requires=">=3.6",
    install_requires=[  
        "requests",  
        "urllib3",
        "jinja2"
    ],
)
