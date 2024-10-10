from setuptools import setup, find_packages
setup(
    name="arshad_hello",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts":["arshad=arshad_hello:hello",],
    }
)