from setuptools import setup, find_packages

setup(
    name="bits",
    version="1.0",
    #    package_dir={"": "src"},
    packages=["bits", "bits.hw", "bits.sw"],
    include_package_data=True,
    install_requires=["click", "pyyaml", "pytest", "tabulate", "myhdl"],
    entry_points="""
        [console_scripts]
        bits=bits:cli
    """,
)
