from setuptools import setup, find_packages

setup(
    name="alpha-connector",  # The name of your package
    version="0.1.0",  # Initial version
    packages=find_packages(),  # Automatically find and include your module
    author="Harshit Bhatia",  # Your name
    author_email="bhatiaharshit07@gmail.com",  # Your email
    description="A package to interact with Alpha Platfrom from Harshit Bhatia",  # A short description
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type="text/markdown",
    url="https://github.com/bhatiaharshit07/alpha-connector",  # URL of the project (optional)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
