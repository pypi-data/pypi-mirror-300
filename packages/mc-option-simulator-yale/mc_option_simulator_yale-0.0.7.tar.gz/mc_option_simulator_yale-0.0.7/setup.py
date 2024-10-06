from setuptools import setup, find_packages
import pathlib


HERE = pathlib.Path(__file__).parent
README = (HERE / "readme.md").read_text(encoding="utf-8")

setup(
    name="mc-option-simulator-yale",
    version="0.0.7",
    packages=find_packages(where="src"),  
    package_dir={"": "src"},  
    entry_points={
        "console_scripts": [
            "montecarlo=montecarlo.MonteCarloSimulation:main",  
        ],
    },
    install_requires=[
        "numpy",
        "scipy",
    ],
    python_requires='>=3.8',
    description="CLI for Geometric Brownian Motion and Black Scholes Math for Monte Carlo Simulation",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Chase Coogan",
    author_email="chasecoogan12@gmail.com",
    license="MIT",
    url="https://github.com/yalehacks/MonteMath",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering",
    ],
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/yalehacks/MonteMath",
        "Source": "https://github.com/yalehacks/MonteMath",
    },
)
