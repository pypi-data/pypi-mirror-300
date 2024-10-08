from setuptools import setup, find_packages

setup(
    name="sab",  # The name of your package
    version="0.1.0",  # Version number
    packages=find_packages(),  # Automatically find the package in the current directory
    install_requires=[  # Dependencies
        # Example: 'numpy>=1.18.0',
    ],
    author="sab",
    author_email="sabavarfr@gmail.com",
    description="quick sab module",
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',  # Tells PyPI that README is in Markdown
    url="https://github.com/yourusername/my_module",  # Project URL (GitHub, etc.)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Python version requirement
)