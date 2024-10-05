import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CMAT-astro",
    version="0.0.1",
    author="Zhang Zixin",
    author_email="troyzx@icloud.com",
    description='''Companion MAss from Ttv modeling:
                a fast to constrain upper mass
                of the hidden companion from TTV data.''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/troyzx/CMAT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
