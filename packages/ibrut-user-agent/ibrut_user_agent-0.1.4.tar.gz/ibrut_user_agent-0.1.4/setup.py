from setuptools import setup, find_packages

setup(
    name="ibrut_user_agent",
    version="0.1.4",
    description="Random instagram useragent app",
    author="Khamdihi dev",
    author_email="dihidev.id@gmail.com",
    url="https://github.com/khamdihi-dev/ibrut_user_agent",  
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
