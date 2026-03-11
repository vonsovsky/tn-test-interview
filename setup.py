from setuptools import setup, find_packages

setup(
    author="Olivie Franklová",
    author_email="olivie.franklova@turbonext.ai",
    name="tn-test-interview",
    version="0.1.0",
    py_modules=["main"],
    install_requires=[
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "app = tn_test_interview.main:main",
        ],
    },
)

