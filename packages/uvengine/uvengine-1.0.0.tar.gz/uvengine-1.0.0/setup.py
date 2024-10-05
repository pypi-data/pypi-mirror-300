import setuptools

setuptools.setup(
    name="uvengine",
    version="1.0.0",
    author="Jose Miguel Horcas",
    author_email="horcas@uma.es",
    description="Variability resolution engine for UVL models and text-based implementation artifacts.",
    long_description="This package provides a variability resolution engine for UVL models and text-based implementation artifacts. It is based on Jinja2 templates and a mapping model that relates the features in the UVL model with the implementation artifacts.",
    long_description_content_type="text/markdown",
    url="https://github.com/jmhorcas/spl_implementation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        'flamapy~=1.1.3',
        'flamapy-fm~=1.1.3',
        'Jinja2~=3.1.3'
    ]
)