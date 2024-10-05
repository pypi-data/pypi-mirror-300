import os
from setuptools import setup, find_packages, Extension

NAME = "sha256sr"
DESCRIPTION = "the secure random generator based on SHA256"
URL = "https://github.com/capricornsky0119/sha256sr.git"
EMAIL = "zhangdaode0119@gmail.com"
AUTHOR = "zhangdaode"

root_dir = os.path.split(os.path.realpath(__file__))[0]
requires_list = open(f"{root_dir}/requirements.txt", "r").readlines()
requires_list = [i.strip() for i in requires_list]

with open(f"{root_dir}/README.md", "r") as fh:
    long_description = fh.read()


example_module = Extension(
    "_secure_random",
    sources=[
        "sha256sr/secure_random.cpp",
        "sha256sr/sha256.cpp",
        "sha256sr/swig_wrap.cxx",
    ],
    include_dirs=["sha256sr/"],
    extra_compile_args=['-std=c++11'],
)

setup(
    name=NAME,
    version="0.1.0",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    packages=find_packages(),
    install_requires=requires_list,
    include_package_data=True,
    zip_safe=False,
    ext_modules=[example_module]
)
