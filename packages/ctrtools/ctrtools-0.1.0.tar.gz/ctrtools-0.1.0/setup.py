from distutils.core import setup
from ctrtools import __version__ as version

long_description = None
with open("readme.md", "r") as f:
    long_description = f.read()

setup(
    name="ctrtools",
    version=version,
    description="A library for working with Homebrew for the Nintendo® 3DS™",
    long_description=long_description,
    long_description_content_type="text/markdown" if long_description else None,
    url="https://github.com/felixwolf/ctr-tools",
    author="Félix",
    author_email="felix.wolfz@gmail.com",
    packages=["ctrtools"],
    entry_points={
        'console_scripts': [
            'ctricon=ctrtools.runnables.ctricon:main',  # Command name and function path
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers", 
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: zlib/libpng License",
        "Topic :: Software Development :: Libraries"
    ]
)
