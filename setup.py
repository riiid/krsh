from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="krsh",
    version="1.0.0-alpha",
    author="AIOps Squad, Riiid Inc",
    url="https://github.com/riiid/krsh",
    download_url="https://github.com/riiid/krsh/archive/master.zip",
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    include_package_data=True,
    keywords=["kubeflow", "krsh", "krsh"],
    install_requires=[],
    entry_points="""
        [console_scripts]
        krsh=krsh.cmd.cli:cli
    """,
    python_requires=">=3.7",
)
