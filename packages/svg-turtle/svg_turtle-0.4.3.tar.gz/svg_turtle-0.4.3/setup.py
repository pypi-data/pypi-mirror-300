"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import setuptools

with open("README.md") as f:
    long_description = f.read()
about = {}
with open("svg_turtle/about.py") as f:
    exec(f.read(), about)

# noinspection PyUnresolvedReferences
setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about['__url__'],
    packages=setuptools.find_packages(),
    install_requires=['svgwrite'],
    classifiers=[  # from https://pypi.org/classifiers/
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"],
    project_urls={
        'Bug Reports': 'https://github.com/donkirkby/svg-turtle/issues',
        'Source': 'https://github.com/donkirkby/svg-turtle'})
