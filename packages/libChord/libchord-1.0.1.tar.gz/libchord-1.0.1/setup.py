from setuptools import setup, find_packages

setup(
    name="libChord",
    version="1.0.1",
    author="Dheekshith Mekala (Arth9r)",
    author_email="dheekshithdev98@gmail.com",
    description="This library offers seamless implementation of Chord Protocol. With just as little as two functions "
                "you can have a fully functioning decentralized chord network. "
                "Read long description to understand how chord protocol works.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DheekshithDev/libChord",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.6',
    install_requires=[
        # List external dependencies only which are not part of standard python library
        "loguru~=0.7.2",
        "cryptography~=43.0.1",
    ],
)

