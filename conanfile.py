from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout

class ISMRMRDConan(ConanFile):
    name = "ismrmrd"
    version = "1.14.2"
    license = "MIT"
    author = "ISMRMRD Community"
    url = "https://github.com/ismrmrd/ismrmrd"
    description = "ISMRMRD: A common data format for MRI raw data."
    topics = ("MRI", "medical imaging", "data format")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "use_hdf5": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "use_hdf5": True,
    }

    exports_sources = "CMakeLists.txt", "schema/*", "libsrc/*", "include/*", "utilities/*", "examples/*", "tests/*"

    requires = [
        "hdf5/1.14.1",
        "pugixml/1.13",
        "boost/1.83.0",
        "fftw/3.3.10"
    ]

    def configure(self):
        self.options["boost"].header_only = False
        self.options["boost"].shared = True
        self.options["boost"].without_random = False
        self.options["boost"].without_test = False
        self.options["boost"].without_system = False
        self.options["boost"].without_filesystem = False
        self.options["boost"].without_program_options = False

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["USE_HDF5_DATASET_SUPPORT"] = "ON" if self.options.use_hdf5 else "OFF"
        tc.variables["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        tc.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["ismrmrd"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.resdirs = ["share/ismrmrd"]
