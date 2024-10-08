import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyGarufa",
    version="0.0.3",
    author="Diego Garbiglia",
    author_email="diegogarbiglia@gmail.com",
    description="Python connector for ROFEX's Rest and Websocket APIs. For multiples comitentes",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/garufa-invex/pyGarufa",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests>=2.20.0',
        'simplejson>=3.10.0',
        'enum34>=1.1.6',
        'websocket-client>=1.6.4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development"
    ],
)