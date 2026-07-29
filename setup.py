"""AMBench — Unified Benchmark for Agent Memory Systems."""

from setuptools import setup, find_packages

setup(
    name="ambench",
    version="0.1.0",
    description="Unified benchmark for agent memory systems spanning all 27 taxonomy cells",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tobias Weiß",
    url="https://github.com/tobias-weiss-ai-xr/agent-memory-bench",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=["pyyaml>=6.0"],
    extras_require={
        "api": ["openai>=1.0"],
        "dev": ["pytest>=8.0"],
        "all": ["openai>=1.0", "pytest>=8.0"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
