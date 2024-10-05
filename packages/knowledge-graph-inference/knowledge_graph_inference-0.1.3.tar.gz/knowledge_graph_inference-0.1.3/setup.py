import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


# Get the long description from the README file.
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="knowledge-graph-inference",
    author="Blue Brain Project, EPFL",
    # use_scm_version={
    #     "relative_to": __file__,
    #     "write_to": "inference_tools/version.py",
    #     "write_to_template": "__version__ = '{version}'\n",
    # },
    version="v0.1.3",
    description="Tools for performing knowledge inference.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="ontology knowledge graph data science",
    packages=find_packages(),
    python_requires=">=3.7,<3.10",
    include_package_data=True,
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
        "nexusforge"
    ],
    extras_require={
        "dev": [
            "tox==4.13.0"
        ],
        "docs": ["sphinx", "sphinx-bluebrain-theme"],
    },
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English",
    ]
)
