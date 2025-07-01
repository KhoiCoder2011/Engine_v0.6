from setuptools import setup, Extension
import pybind11


pybind11_include = pybind11.get_include()


extension = Extension(
    name='Math',
    sources=['Math/math.cpp'],
    include_dirs=[pybind11_include, "D:\Dev\Python\Engine\ForgeX Engine\source\Include"],
    language='c++'
)

setup(
    name='Math',
    version='0.1',
    ext_modules=[extension],
    zip_safe=False,
)
