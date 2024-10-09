from setuptools import setup, find_packages
import os

# Install fluidsynth using apt
os.system('apt-get update && apt-get install -y fluidsynth')

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="musecraft",
    version="24.10.8",
    description="Front-end for symbolic music AI models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alex Lev",
    author_email="alexlev61@proton.me",
    url="https://github.com/asigalov61/MuseCraft",  # Add the URL of your project
    project_urls={
        "Issues": "https://github.com/asigalov61/MuseCraft/issues",
        "Documentation": "https://github.com/asigalov61/MuseCraft/docs",
        "Discussions": "https://github.com/asigalov61/MuseCraft/discussions",
        "Source Code": "https://github.com/asigalov61/MuseCraft",
    },
    packages=find_packages(),  # Automatically find and include all packages
    include_package_data=True,
    install_requires=[
        'tqdm',
        'pillow',
        'numpy',
    ],
    keywords=['MIDI', 'musecraft', 'music ai'],  # Add your keywords here
    python_requires='>=3.6',  # Specify the Python version
    license='Apache Software License 2.0',  # Specify the license
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',  
        'Operating System :: OS Independent',        
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
)
