import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='vodscrepe',
    version='0.0.6',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    description='Vods.co Vod Scraper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Dawson Booth',
    author_email='pypi@dawsonbooth.com',
    url='https://github.com/dawsonbooth/vodscrepe',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    license='MIT',
)
