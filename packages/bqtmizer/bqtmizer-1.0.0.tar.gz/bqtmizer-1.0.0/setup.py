import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="bqtmizer",
    version="1.0.0",
    author="Xinyi Wang",
    author_email="xinyi@simula.no",
    description="BQTmizer: A Tool for Test Case Minimization with Quantum Annealing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/qiqihannah/BQTmizer",
    classifiers= ["Programming Language :: Python :: 3",  # 编程语言
        "License :: OSI Approved :: MIT License",  # license
        "Operating System :: OS Independent"],  # 操作系统
    install_requires=[
        "dimod==0.12.17",
        "dwave-system==1.26.0",
        "dwave-inspector==0.5.1",
        "pandas",
    ],
    package_data={"pipmodule": ["*.png", ]},
    python_requires=">=3.8",
)