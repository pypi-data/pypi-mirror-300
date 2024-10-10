
from setuptools import setup, find_packages


setup(
    name='qr-code-reader',
    version='1.1.1',  # Increment the version number here
    packages=find_packages(),
    description='A simple QR code reader',
    author='DEVMNE',
    author_email='mne@yaposarl.ma',
    url='https://github.com/mnedev-cell/qr_code_reader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

