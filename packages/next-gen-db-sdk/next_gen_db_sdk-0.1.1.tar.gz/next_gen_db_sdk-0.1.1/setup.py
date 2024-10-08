from setuptools import setup, find_packages

setup(
    name="next-gen-db-sdk",  # The name of your package
    version="0.1.1",  # Initial version of your package
    packages=find_packages(),  # Automatically find packages
    install_requires=["requests"],  # Dependencies your package needs
    description="Python SDK to interact with next-gen-db",  # Short description
    long_description=open("README.md", "r").read(),  # Include README.md as long description
    long_description_content_type="text/markdown",  # Specify the format of the long description
    author="Ayush Parida",  # Author name
    author_email="ayushparida999@gmail.com",  # Author email
    url="https://github.com/ayush-parida/next-gen-db-sdk.git",  # URL of your project
    classifiers=[  # Optional classifiers for better categorization on PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Use an appropriate license classifier
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the minimum supported Python version
)

