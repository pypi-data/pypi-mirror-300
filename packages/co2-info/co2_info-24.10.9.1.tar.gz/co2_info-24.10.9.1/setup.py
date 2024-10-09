import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="co2_info",
    version="24.10.9.1",
    packages=setuptools.find_packages(),
    install_requires=['argparse', 'paho.mqtt>=2', 'uuid', 'pandas', 'matplotlib', 'urllib3'],
    author="Peter Vennemann",
    author_email="vennemann@fh-muenster.de",
    description="A simple alert app for indoor air quality.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.fh-muenster.de/pv238554/co2_info",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
