import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="iran_kish_py",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'pycryptodome',
        'requests',
        'urllib3<2'
    ],
    tests_require=[
        'unittest',
    ],
    test_suite='tests',
    description="Iran Kish payment portal python package",
    long_description=README,
    long_description_content_type="text/markdown",
    author="fastpanda99",
    author_email="fastpanda99@gmail.com",
    url="https://fastpanda99.github.io/iran_kish_py/",
)
