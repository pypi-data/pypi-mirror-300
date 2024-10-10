from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='keelib',
    version='0.1.3',
    description='KEE by Jaegerwald, but as a library.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='TheZoidMaster',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'colorama'
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    project_urls={
        "Source": "https://github.com/TheZoidMaster/keelib",
        "Original": "https://github.com/JaegerwaldDev/KEE"
    }
)
