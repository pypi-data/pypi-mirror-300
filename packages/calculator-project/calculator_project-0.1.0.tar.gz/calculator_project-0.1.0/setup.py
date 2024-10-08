from setuptools import setup, find_packages

setup(
    name="calculator_project",
    version="0.1.0",
    description="A simple calculator to perform basic arithmetic operations and root calculations.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Mustafa Akgül",
    author_email="akgul037@gmail.com",
    url="https://github.com/mustafaakgl/Calculator1",  # Update with your project's URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
