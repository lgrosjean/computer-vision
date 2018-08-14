import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mask_rcnn",
    version="0.0.1",
    author="Leo Grosjean",
    author_email="leo.grosjean@ekimetrics.com",
    description="Object detection based on mask_rcnn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lgrosjean",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Ekimetrics",
        "Operating System :: OS Independent",
    ),
)