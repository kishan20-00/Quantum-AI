from setuptools import setup, find_packages

setup(
    name="quantum-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "aiohttp>=3.8.0",
        "tenacity>=8.2.0",
        "pydantic>=1.10.0"
    ],
    python_requires=">=3.7",
)