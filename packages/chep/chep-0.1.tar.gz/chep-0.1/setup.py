
from setuptools import setup, find_packages

setup(
    name="chep",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Jose Corcios",
    author_email="corciosv@gmail.com",
    description="Un paquete para extraer el puerto SSH del servicio chep",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/jose503/chep",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
