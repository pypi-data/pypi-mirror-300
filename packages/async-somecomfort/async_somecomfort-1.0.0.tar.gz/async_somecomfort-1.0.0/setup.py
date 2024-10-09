from setuptools import setup, find_packages

setup(
    name="async-somecomfort",  # Update this to the actual package name you'd like
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python client for interacting with Honeywell Total Connect Comfort (TCC) API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/async-somecomfort",  # Replace with your repository URL
    packages=find_packages(),  # Automatically finds and includes your Python packages
    install_requires=[
        "aiohttp>=3.7.4",  # Include dependencies like aiohttp
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
