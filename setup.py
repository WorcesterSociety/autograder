from setuptools import setup, find_packages

setup(
    name="grader",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["docker>=2", "rarfile>=3", "sh>=1"],
    tests_require=["pytest"]
)
