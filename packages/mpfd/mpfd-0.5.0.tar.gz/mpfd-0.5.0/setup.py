from setuptools import setup, find_packages

setup(
    name="mpfd",                             # Package name
    version="0.5.0",                         # Initial version
    description="A decorator that makes a function into a parallel processor using multithreading.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # Ensures the README is interpreted as markdown
    author="Pranav Hirani",                      # Replace with your name
    author_email="pranavpatel7260@gmail.com",   # Replace with your email
    url="https://github.com/alloc7260/mpfd",  # Optional: Replace with your GitHub repository link
    license="MIT",                           # License type
    packages=find_packages(),                # Automatically discover all packages in the project
    classifiers=[                            # Additional package metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',                 # Minimum Python version
)
