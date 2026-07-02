from setuptools import setup, find_packages

setup(
    name="wtective",
    version="1.0.0",
    description="A highly accurate, universal CLI tool for web technology detection.",
    author="OnurDemir1",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.27",
        "beautifulsoup4>=4.12",
        "dnspython>=2.6",
        "mmh3>=4.1",
        "rich>=13.7",
    ],
    extras_require={
        "dev": ["pytest>=8.0"],
    },
    entry_points={
        "console_scripts": [
            "wtect=wtective.main:main",
            "wtective=wtective.main:main",
            "wt=wtective.main:main",
        ],
    },
)
