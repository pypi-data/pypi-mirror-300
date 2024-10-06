from setuptools import setup

setup(
    name="MINSGA3",
    version='1.1',
    author="Shayan Firouzian H.",
    url="",
    python_requires='>=3.9',
    description="A modification of Pymoo library's NSGA3 algorithm to work with Mixed-Integer problems",
    license='Open Software License v. 3.0 (OSL-3.0)',
    include_package_data=True,
    exclude_package_data={
        '': ['*.c', '*.cpp', '*.pyx'],
    },
    install_requires=['pymoo>=0.6.1.3'],
    platforms='any'
)