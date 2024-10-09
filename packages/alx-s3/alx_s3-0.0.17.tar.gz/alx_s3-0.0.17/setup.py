import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alx-s3",
    version="0.0.17",
    author="sairamn",
    author_email="sairam.n90@gmail.com",
    description="Dummy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/my-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)