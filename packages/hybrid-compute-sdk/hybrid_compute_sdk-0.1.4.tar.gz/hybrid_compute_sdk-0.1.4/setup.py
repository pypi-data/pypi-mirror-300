from setuptools import setup, find_packages

setup(
    name="hybrid_compute_sdk",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "jsonrpcserver",
        "aiohttp",
    ],
    author="Boba",
    author_email="",
    description="A Python SDK for creating JSON-RPC servers with hybrid compute capabilities",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bobanetwork/aa-hc-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
