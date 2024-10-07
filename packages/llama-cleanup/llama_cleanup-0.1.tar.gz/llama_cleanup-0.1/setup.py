from setuptools import setup, find_packages

setup(
    name="llama-cleanup",  # Replace with your package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "langchain_ollama"
    ],
    include_package_data=True,  # Include files like config.json
    description="A package to process addresses and filter out noise",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Andrew",
    author_email="gordienko.adg@gmail.com",
    url="https://github.com/AndrewGordienko/address-cleanup",  # Replace with your project URL if hosted on GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'my_package_process=my_package.main:process_addresses',
        ],
    },
    python_requires='>=3.8',
)

