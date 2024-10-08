from setuptools import setup

# Reading the long description from README.md
with open("README.md", "r", encoding="utf-8") as rd:
    long_description = rd.read()

setup(
    name="bonggoQuery",
    version="2.0.2.1",
    description="A package that helps you perform various operations, especially for building virtual assistants.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SudipBera083",
    author="Sudip Bera",
    author_email="sudipbera083@gmail.com",
    packages=['bonggoQuery'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "wolframalpha",
        "pyttsx3",
        "SpeechRecognition",
        "wikipedia"
    ],
    python_requires='>=3.6',
    license="MIT",
    keywords="virtual assistant query voice python",
    project_urls={
        "Bug Tracker": "https://github.com/SudipBera083/issues",
        "Source Code": "https://github.com/SudipBera083/BonggoQuery",
    },
    package_data={
        "bonggoQuery": ["assets/logo.png"],  # Adjust path to where the logo is located
    },
    include_package_data=True,  # Ensure non-code files are included
)
