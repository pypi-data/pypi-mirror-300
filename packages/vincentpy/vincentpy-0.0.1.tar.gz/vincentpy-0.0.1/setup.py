from setuptools import setup, find_packages

# Setting up
setup(
    name="vincentpy",
    version="0.0.1",
    author="Vincent Viljoen",
    author_email="vv@gmail.com",
    description="Test custom package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
