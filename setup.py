from setuptools import find_packages, setup

with open("app/Readme.md", "r") as fh:
    long_description = fh.read()
    
    
setup (
    name="svlib",
    version="0.0.10",
    description="A simple library containing abstract base classes for motors, and some pre-defined UI elements",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snhig/SvLib",
    author="Sean Higley",
    author_email="snhigley@gmail.com",
    license="BSD-3-Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy >= 1.24.2",
                      "opencv-python >= 4.8",
                      "pyqtgraph >= 0.13.3",
                      "PySide6 >= 6.5.1",
                      "PySide6_Addons >= 6.5.1",
                      "PySide6_Essentials >= 6.5.1",
                      "nd2 >= 0.10.1", 
                      ],
    python_requires='>=3.10',
   
)