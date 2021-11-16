import os
import pathlib

from conans import ConanFile, tools
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
from conan.tools.layout import cmake_layout
from conan.tools.files import AutoPackager

required_conan_version = ">=1.42"

class CuraEngineConan(ConanFile):
    name = "curaengine"
    version = "4.13.0-alpha+001"
    license = "AGPL-3.0"
    author = "Ultimaker B.V."
    url = "https://github.com/Ultimaker/CuraEngine"
    description = "Powerful, fast and robust engine for converting 3D models into g-code instructions for 3D printers. It is part of the larger open source project Cura."
    topics = ("conan", "cura", "protobuf", "gcode", "c++", "curaengine", "libarcus", "gcode-generation")
    settings = "os", "compiler", "build_type", "arch"
    revision_mode = "scm"
    build_policy = "missing"
    default_user = "ultimaker"
    default_channel = "testing"
    exports = "LICENSE*"
    options = {
        "enable_arcus": [True, False],
        "enable_openmp": [True, False],
        "tests": [True, False]
    }
    default_options = {
        "enable_arcus": True,
        "enable_openmp": True,
        "tests": False
    }
    scm = {
        "type": "git",
        "subfolder": ".",
        "url": "auto",
        "revision": "auto"
    }

    def config_options(self):
        if self.settings.os == "Macos":
            self.options.enable_openmp = False

    def configure(self):
        if self.options.enable_arcus:
            self.options["arcus"].shared = True
            self.options["protobuf"].shared = self.settings.os != "Macos"
        self.options["clipper"].shared = True

    def build_requirements(self):
        if self.options.enable_arcus:
            self.build_requires("protobuf/3.17.1")
        if self.options.tests:
            self.build_requires("gtest/[>=1.10.0]", force_host_context = True)

    def requirements(self):
        self.requires("stb/20200203")
        if self.options.enable_arcus:
            self.requires(f"arcus/4.13.0-alpha+001@ultimaker/testing")
            self.requires("protobuf/3.17.1")
        self.requires("clipper/6.4.2")
        self.requires("rapidjson/1.1.0")

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, 17)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        cmake = CMakeDeps(self)
        cmake.generate()

        tc = CMakeToolchain(self)

        # FIXME: This shouldn't be necessary (maybe a bug in Conan????)
        if self.settings.compiler == "Visual Studio":
            tc.blocks["generic_system"].values["generator_platform"] = None
            tc.blocks["generic_system"].values["toolset"] = None

        tc.variables["ALLOW_IN_SOURCE_BUILD"] = True
        tc.variables["ENABLE_ARCUS"] = self.options.enable_arcus
        tc.variables["BUILD_TESTS"] = self.options.tests
        tc.variables["ENABLE_OPENMP"] = self.options.enable_openmp
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        packager = AutoPackager(self)
        packager.patterns.build.bin = ["CuraEngine", "CuraEngine.exe"]
        packager.run()

    def package_info(self):
        if self.in_local_cache:
            self.runenv_info.prepend_path("PATH", os.path.join(self.folders.package, "bin"))
        else:
            self.runenv_info.prepend_path("PATH", self.folders.build)

    def package_id(self):
        self.info.requires.full_version_mode()
