from setuptools import find_packages, setup

setup(
    name="BingImageCreator-fork",
    version="0.8.2",
    license="GNU General Public License v2.0",
    author="Antonio Cheong, yihong0618",
    author_email="acheong@student.dalat.org, zouzou0208@gmail.com",
    description="High quality image generation by Microsoft. Reverse engineered API.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/yihong0618/BingImageCreator",
    project_urls={
        "Bug Report": "https://github.com/yihong0618/BingImageCreator/issues/new",
    },
    install_requires=[
        "httpx",
        "regex",
        "requests",
        "fake-useragent",
        "curl_cffi",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["BingImageCreator"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
