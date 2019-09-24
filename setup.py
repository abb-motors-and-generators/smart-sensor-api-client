import setuptools

# Read in the package description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

# Add the required packages
requirements_path = 'requirements.txt'
install_requires = []
with open(requirements_path) as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="smart_sensor_client",
    version="0.0.1",
    author="ABB Switzerland Ltc.",
    author_email="ch-support.cloudinterface.smartsensor@abb.com",
    description="A library to access the ABB Ability Smart Sensor Cloud Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abb-motion/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License 3-Clause License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
)
