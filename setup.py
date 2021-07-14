import os
import re
import subprocess
import sys
from distutils.version import LooseVersion
from importlib.util import find_spec

from setuptools import setup, Extension, Command
from setuptools.command.build_ext import build_ext
from setuptools.command.test import test as TestCommand

from package_info import PackageInfo


# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}

# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cfg = "Debug" if self.debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(extdir),
            "-DPYTHON_EXECUTABLE={}".format(sys.executable),
            "-DPYQUBO_VERSION_INFO={}".format(self.distribution.get_version()),
            "-DCMAKE_BUILD_TYPE={}".format(cfg),  # not used on MSVC, but no harm
        ]
        build_args = []

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator:
                try:
                    import ninja  # noqa: F401

                    cmake_args += ["-GNinja"]
                except ImportError:
                    pass

        else:

            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                    "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
                ]
                build_args += ["--config", cfg]

        if sys.platform.startswith("darwin"):
            # disable macos openmp since addtional dependency is needed.
            if (not {'True': True, 'False': False}[os.getenv('USE_OMP', 'False')]):
                cmake_wargs += ['-DUSE_OMP=No']
            # Cross-compile support for macOS - respect ARCHFLAGS if set
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            if archs:
                cmake_args += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += ["-j{}".format(self.parallel)]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )
        
class GoogleTestCommand(TestCommand):
    """
    A custom test runner to execute both Python unittest tests and C++ Google Tests.
    """
   def initialize_options(self):
        self.cpplibdir = self.distutils_dir_name()

   def finalize_options(self):
        pass

   user_options = []

   def distutils_dir_name(self):
        """Returns the name of a distutils build directory"""
        f = "temp.{platform}-{version[0]}.{version[1]}"
        return f.format(platform=sysconfig.get_platform(),
                        version=sys.version_info)

    def run(self):
        # Run Python tests
        super(GoogleTestCommand, self).run()
        print("\nPython tests complete, now running C++ tests...\n")
        # Run catch tests
        print(os.path.join('build/', self.cpplibdir))
        subprocess.call(['make pyqubo_test'],
                        cwd=os.path.join('build', self.cpplibdir), shell=True)
        subprocess.call(['./tests/pyqubo_test'],
                        cwd=os.path.join('build', self.cpplibdir), shell=True)

class PyTestCommand(TestCommand):
    def run(self):
        super().run()


package_info = PackageInfo(os.path.join('pyqubo', 'package_info.py'))       
        

setup(
        name=package_info.__package_name__,
        version=package_info.__version__,
        description=package_info.__description__,
        long_description=open('README.rst').read(),
        author=package_info.__contact_names__,
        author_email=package_info.__contact_emails__,
        maintainer=package_info.__contact_names__,
        maintainer_email=package_info.__contact_emails__,
        url=package_info.__repository_url__,
        download_url=package_info.__download_url__,
        license=package_info.__license__,
        ext_modules=[CMakeExtension('pyqubo')],
        cmdclass=dict(build_ext=CMakeBuild, test=GoogleTestCommand, pytest=PyTestCommand),
        keywords=package_info.__keywords__,
        )
