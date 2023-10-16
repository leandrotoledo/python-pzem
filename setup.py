from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-pzem",
    version="0.1.5",
    author="Leandro Muto, Leandro Toledo",
    author_email="leandro.muto@gmail.com, leandrotoledodesouza@gmail.com",
    description="Python interface for PZEM-014 and PZEM-016 Energy Meters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leandrotoledo/python-pzem",
    project_urls={
        "Bug Tracker": "https://github.com/leandrotoledo/python-pzem/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="LGPLv3",
    packages=["pzem"],
    install_requires="minimalmodbus",
    python_requires=">=3.6",
)
