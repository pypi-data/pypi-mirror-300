from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='SendEmailPy3',
    packages=['sendemailpy3'],
    version="1.1.0",
    license="MIT",
    description="Easy email sending for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Goutham Narayana Pedinedi",
    author_email="codspecialops@gmail.com",
    url="https://github.com/GouthamOfTheNP/send_email",
    keywords=["send", "email", "python",],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)