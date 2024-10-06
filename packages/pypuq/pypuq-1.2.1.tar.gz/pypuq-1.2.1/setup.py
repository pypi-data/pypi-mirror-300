import os
import subprocess
import sys
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class CMakeBuild(build_ext):
    def run(self):
        # Ensure CMake is installed
        try:
            subprocess.check_call(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = Path(self.get_ext_fullpath(ext.name)).parent.resolve()
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCODE_VERSION={os.getenv('CODE_VERSION')}",
        ]
        
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'], cwd=self.build_temp)

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

setup(
    name='pypuq',
    version=os.getenv('CODE_VERSION'),
    author=os.getenv('CODE_AUTHOR'),
    description=os.getenv('CODE_DESCRIPTION'),
    long_description='C++ implementation of physical units and quantities and their conversions.',
    ext_modules=[CMakeExtension('pypuq')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    packages=setuptools.find_packages(),
    include_package_data=True,
)
