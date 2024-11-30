from setuptools import setup, find_packages

setup(
    name="markdown-html",  # Replace with the actual name of your package
    version="0.1.0",  # Version of your package
    author="SwapCodesDev",  # Replace with your name
    author_email="swapcodes.dev@gmail.com",  # Replace with your email
    description="A Python package for converting Markdown to HTML",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SwapCodesDev/Markdown-to-HTML",
    py_modules=["markdown"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Match the LICENSE file
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['beautifulsoup4', 'emoji'],  # Add dependencies here if needed
    package_data={'markdown':['README.md', 'LICENSE']},
    license="MIT",
)
