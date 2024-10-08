from setuptools import setup, find_packages

setup(
    name="simple-user-creation",  # The name of your package
    version="0.1.0",  # Initial version
    packages=find_packages(),
    install_requires=["requests"],  # Dependencies your package needs
    description="An SDK for creating users",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/your_username/your_sdk",  # URL of your project
    author="Adithya k",
    author_email="adithya.k@setu.co",
    license="MIT",  # License type
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
)
