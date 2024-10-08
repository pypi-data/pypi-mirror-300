# setup.py
from setuptools import setup, find_packages

setup(
    name="cybersift_sdk",          # Package name
    version="0.1.3.4",               # Initial version
    packages=find_packages(),      # Automatically find the package
    author="CyberSift",
    author_email="david.vassallo@cybersfit.io",
    description="A python helper for the various CyberSift APIs",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',     # Python version requirement
    test_suite='tests',          # Points to the tests folder
    install_requires=['requests', 'python-dotenv', 'build'],
)
