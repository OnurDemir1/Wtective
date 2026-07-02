from setuptools import setup, find_packages

setup(
    name="wtective",
    version="1.0.0",
    description="A highly accurate, universal CLI tool for web technology detection.",
    author="OnurDemir1",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "httpx==0.27.0",
        "beautifulsoup4==4.12.3",
        "dnspython==2.6.1",
        "mmh3==4.1.0",
        "rich==13.7.1",
        "pillow==10.2.0"
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
