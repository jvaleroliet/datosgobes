from setuptools import setup, find_packages

setup(
    name="datosgobes",
    description="Python package to access Spanish Government Open Data from the datos.gob.es API",
    version="0.1.2",
    author="Juan Valero",
    author_email="olietvalero@gmail.com",
    url="https://github.com/jvaleroliet/datosgobes",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.0",
        "requests>=2.31.0",
        "numpy==1.26.4"
    ],
    python_requires=">=3.9",
)
