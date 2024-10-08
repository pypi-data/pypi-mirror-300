from setuptools import setup, find_packages

setup(
    name="zsvg",
    author="zm741234",
    version="0.1.0.20",
    packages=find_packages(),
    description="A svg utilities package",
    long_description="A svg utilities package",
    long_description_content_type="text/markdown",
    package_data={
        "zsvg": [
            "sec.cpython-312-darwin.so",
            "load.cpython-312-darwin.so",
            "sleep.cpython-312-darwin.so",
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
