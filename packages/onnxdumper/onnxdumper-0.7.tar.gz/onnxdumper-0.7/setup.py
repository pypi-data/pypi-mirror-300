from setuptools import setup, find_packages

setup(
    name="onnxdumper",
    version="0.7",
    packages=find_packages(),
    install_requires=[
        "onnx",
        "onnxruntime",
        "numpy",
    ],
    author="Souls-R",
    author_email="2362912722@qq.com",
    description="A package for ONNX intermediate data dumping",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)