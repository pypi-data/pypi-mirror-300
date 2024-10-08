from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='mpra',  # Your package name
    version='0.1.1',
    description='MPRA - Multipurpose Resource Automation',
    long_description=long_description,  # Description from the README file
    # Use 'text/x-rst' if you use .rst file
    long_description_content_type='text/markdown',
    url='https://github.com/ManojPennada/mpra',  # Your project URL
    author='Manoj Pennada',
    author_email='manojpennada@gmail.com',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
