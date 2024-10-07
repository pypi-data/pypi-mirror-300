from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lingopy',
    version='0.1.0.1',
    description=
    'Lingopy is a lightweight localization library for Python that helps you manage localized messages effortlessly.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Maksymilian Sawicz',
    url='https://github.com/0x1618/lingopy-python',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
