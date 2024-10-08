from setuptools import setup

setup(
    name="sc_cortado",
    version="0.1.22",
    author="Musaddiq Lodi",
    author_email="lodimk2@vcu.edu",
    description="CORTADO: hill Climbing Optimization foR cell-Type specific mArker gene DiscOvery",
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "pandas",
        "scikit-learn",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lodimk2/cortado",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)