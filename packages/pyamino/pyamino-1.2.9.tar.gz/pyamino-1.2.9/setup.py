from setuptools import setup, find_packages

setup(
    name="pyamino",
    license="MIT",
    author="pyminoTeam",
    author_email="",
    description="Easily create a bot for Amino Apps using a modern easy to use synchronous library.",
    url="https://github.com/forevercynical/pymino",
    version = "1.2.9",
    packages=find_packages(),
    install_requires=[
        "requests==2.31.0",
        "colorama==0.4.6",
        "websocket-client==1.6.1",
        "diskcache==5.6.1"
    ],
    keywords=[
        "amino",
        "pymino",
        "narvii",
        "amino-api",
        "narvii-bots",
        "aminoapps",
        "amino-bot",
        "amino-bots"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8"
)
