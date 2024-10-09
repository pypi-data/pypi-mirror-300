# coding: utf-8
from codecs import open
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="hanpinyin",
    version="0.1.0",
    author="He Mingze",
    author_email="hhhhmdzz1024@gmail.com",
    description="基于 g2pW 使用 torch 推理的 pypinyin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/hhhhmdzz/hanpinyin",
    # project_urls={
    #     "Bug Tracker": "https://github.com/hhhhmdzz/hanpinyin/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    install_requires=['g2pw>=0.1.1', 'pypinyin>=0.47.1'],
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.6, <4',
    include_package_data=True,
)
