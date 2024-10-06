from setuptools import setup, find_packages

setup(
    name="PerforMate",
    version="0.1.4",
    author="Elijah M",
    author_email="elijah@kreateyou.com",
    description="A lightweight performance tracker for python projects.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kreateyou/PerforMate",  # Your GitHub repo link
    packages=find_packages(),
    install_requires=[
        'tinydb',
        'pandas',
        'matplotlib',
        'numpy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
