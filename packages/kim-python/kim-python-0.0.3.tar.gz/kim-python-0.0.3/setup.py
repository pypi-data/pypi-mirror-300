from setuptools import setup, find_packages
import pathlib

current_directory = pathlib.Path(__file__).parent
long_description = (current_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="kim-python",
    version="0.0.3",
    author="milan.dg@free.fr",
    url="https://github.com/Dammmmmm/kim",
    description="A package to Keep In Mind your constants and call them anytime anywhere",
    packages=find_packages(),
    readme = "README.md",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = [],
    python_requires = ">=3.5",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]  
)