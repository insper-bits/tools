from setuptools import setup, find_packages

setup(
    name="bits",
    version="1.0",
    packages=[
        "bits",
        "bits.hw",
        "bits.util",
        "bits.sw.assembler",
        "bits.sw.vmtranslator",
        "bits.sw.simulator",
    ],
    include_package_data=True,
    install_requires=[
        "click",
        "pyyaml",
        "pytest",
        "tabulate",
        "myhdl",
        "wheel",
        "PyQt5",
    ],
    entry_points="""
        [console_scripts]
        bits=bits:cli
    """,
)
