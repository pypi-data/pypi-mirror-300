from setuptools import setup, find_packages

setup(
    name="easyprojectstructure",
    version="0.1",
    packages=find_packages(),
    author="Sergei Poluektov",
    author_email="seregatipich@outlook.com",
    description="A script to output the directory structure of a Python project.",
    url="https://github.com/seregatipich/easyprojectstructure",
    entry_points={
        "console_scripts": [
            "getprojectstructure=easyprojectstructure.__main__:main",
            "easyprojectstructure=easyprojectstructure.__main__:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
