from setuptools import setup, find_packages

setup(
    name="qr_code_reader",  # Your package name
    version="0.1.0",
    description="A simple QR Code Reader utility",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),  # Automatically finds the qr_code_reader package
    install_requires=[],  # Any dependencies can be listed here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
