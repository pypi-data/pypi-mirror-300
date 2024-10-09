from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

setup(
    name="pyrvs",
    version="0.1",
    author="Daniele Bonatto, Sarah Fachada",
    author_email="daniele.bonatto@ulb.be",
    description="Reference View Synthesizer (RVS) python package.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/your_project_name",  # Optional if hosted on GitHub
    license="MIT",  # Specify your license
    cmdclass={"build_ext": build_ext},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
    install_requires=[
        'pybind11>=2.6.0',
        'numpy',
        'opencv-python'
    ],
    packages=find_packages(include=["pyrvs", "pyrvs.*"]),  # Adjust this to your package
)
