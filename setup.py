from setuptools import setup, find_packages

setup(
    name="python-errors",
    version="0.0.5",
    author="Nick",
    author_email="njames.programming@example.com",
    description="A library for reducing and identifying critical errors in Python code.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RoyalGr4pe/python-errors",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    include_package_data=True,
)
