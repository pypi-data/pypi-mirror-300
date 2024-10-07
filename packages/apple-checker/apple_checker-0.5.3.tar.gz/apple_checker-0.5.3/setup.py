from setuptools import setup, find_packages

setup(
    name='apple-checker',
    version='0.5.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'cryptography',
        'requests',
    ],
    author='KupQ',
    description='A package for checking certificates and entitlements',
    long_description="",
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
