from setuptools import setup, find_packages

setup(
    name="drift_shield",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas', 'scipy'
    ],
    author="Shanmukh Dara",
    author_email="shanmukhdara@gmail.com",
    description="A package to monitor and track data drift for ML models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
