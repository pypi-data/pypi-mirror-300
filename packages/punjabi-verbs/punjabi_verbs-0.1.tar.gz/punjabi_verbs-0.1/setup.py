from setuptools import setup, find_packages

setup(
    name="punjabi_verbs",              # Name of your package
    version="0.1",                     # Initial version
    description="A package for Punjabi verbs",  # Short description
    packages=find_packages(),          # Automatically find packages
    include_package_data=True,         # Include non-code files (like verbs.txt)
    install_requires=[],               # List any dependencies here
    author="Muhammad Shoaib Tahir",                # Your name
    author_email="shoaibtahir410@gmail.com",  # Your email
    url="https://github.com/MuhammadshoaibTahir/punjabiverbs.git",  # Link to your repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',           # Python version requirement
)
