from setuptools import setup, find_packages

setup(
    name="rawML",  # Replace with your package name
    version="0.1.1",  # Initial version
    description="Yet another ML library!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jasmer Singh Sanjotra",
    author_email="jasmer.sanjotra@gmail.com",
    url="https://github.com/TheAlphaJas/rawML-Python/",  # Your project repo
    packages=find_packages(),  # Automatically finds your package directories
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or your preferred license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy', 
    ],
)
