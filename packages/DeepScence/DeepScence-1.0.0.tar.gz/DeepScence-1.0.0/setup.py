from setuptools import setup

setup(
    name="DeepScence",
    version="1.0.0",
    description="single-cell and spatial detection of senescent cells",
    author="Anthony Qu",
    author_email="anthonyylq@gmail.com",
    packages=["DeepScence"],
    include_package_data=True,
    package_data={
        "": ["data/*.csv"],
    },
    install_requires=[
        "numpy>=1.7",
        "torch",
        "h5py",
        "six>=1.10.0",
        "scikit-learn",
        "scanpy",
        "kopt",
        "pandas",
    ],
    url="https://github.com/quyilong0402/DeepScence",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
