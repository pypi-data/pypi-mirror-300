import os
import io
import re
import subprocess
from setuptools import setup, find_packages

# Read in README.md to use it for the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()
    
def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "minigrad", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)
    
def get_cuda_version():
    """Attempts to retrieve CUDA version by calling `nvcc --version`."""
    try:
        # Check CUDA version using nvcc
        output = subprocess.check_output(['nvcc', '--version']).decode().strip()
        for line in output.split('\n'):
            if 'release' in line:
                # Extract version number (e.g., 'release 11.2, V11.2.152')
                version = line.split('release')[-1].split(',')[0].strip()
                return version
    except Exception:
        # If nvcc isn't available or there's an error, default to None
        return None

def get_cupy_package():
    """Returns the appropriate CuPy package based on the CUDA version."""
    cuda_version = get_cuda_version()
    if cuda_version:
        major_version = cuda_version.split('.')[0]
        if major_version == '12':
            return 'cupy-cuda12x'
        elif major_version == '11':
            return 'cupy-cuda11x'
        elif major_version == '10':
            return 'cupy-cuda10x'
    return None

def get_install_requires():
    install_requires = get_requirements()
    cupy_package = get_cupy_package()
    if cupy_package:
        install_requires.append(cupy_package)
    return install_requires

setup(
    name="minigrad-python",
    version=get_version(),
    author="Uday Sankar",
    license="MIT",
    description="A minimal deep learning framework with automatic differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udaysankar01/minigrad",
    packages=find_packages(exclude=["test"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=get_install_requires(),
    extras_reqquire={
        "dev": ["pytest", "pytest-benchmark"],
    },
    include_package_data=True

)