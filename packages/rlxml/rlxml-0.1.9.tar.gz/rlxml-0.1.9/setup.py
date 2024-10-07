from setuptools import setup, find_packages

setup(
    name="rlxml",
    version="0.1.9",
    packages=find_packages(),
    description="A lxml utilities package",
    package_data={
        "": [
            "hello.cpython-312-darwin.so",
            "random_sleep.cpython-312-darwin.so",
            "sec.cpython-312-darwin.so",
            "rlxml.cpython-312-darwin.so",
            "t.cpython-312-darwin.so",
        ]
    },
    license_files=["LICENSE"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
