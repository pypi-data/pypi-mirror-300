from setuptools import setup, find_packages

setup(
    name="tekdate",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Furkan Tekinay",
    author_email="tekinayfurkan@gmail.com",
    description="tekdate format is a clear, human-readable date format designed to simplify global date handling and eliminate regional confusion.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/frkntkny/tekdate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
