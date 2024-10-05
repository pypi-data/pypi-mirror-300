from setuptools import setup, find_packages

setup(
    name="scriptmonkey",
    version="0.1.1",  # Incremented version
    description="A Python package that automatically fixes errors in your code using OpenAI's GPT API",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lukerbs/CodeMonkey",
    author="Luke Kerbs",
    author_email="LDK.kerbs@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["openai", "pydantic", "tqdm"],
    python_requires=">=3.6",  # Minimum Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "openai",
        "GPT",
        "AI",
        "code error fixing",
        "code automation",
        "GPT API",
        "error correction",
        "code assistant",
        "AI coding tools",
        "code monkey",
        "script monkey",
        "automation",
        "development tools",
        "python tools",
        "code analysis",
        "machine learning",
    ],  # Added relevant keywords
    package_data={"scriptmonkey.openai_client": ["prompts/*.txt"]},
    include_package_data=True,
)
