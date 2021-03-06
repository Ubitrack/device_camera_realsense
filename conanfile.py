from conans import ConanFile, CMake, tools


class UbitrackCoreConan(ConanFile):
    name = "ubitrack_device_camera_realsense"
    version = "1.3.0"

    description = "Ubitrack Device Camera realsense"
    url = "https://github.com/Ubitrack/device_camera_realsense.git"
    license = "GPL"

    short_paths = True
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    requires = (
        "ubitrack_core/%s@ubitrack/stable" % version,
        "ubitrack_vision/%s@ubitrack/stable" % version,
        "ubitrack_dataflow/%s@ubitrack/stable" % version,
        "librealsense/[=2.17.1]@camposs/stable",
       )

    default_options = (
        "ubitrack_core:shared=True",
        "ubitrack_vision:shared=True",
        "ubitrack_dataflow:shared=True",
        )

    # all sources are deployed with the package
    exports_sources = "cmake/*", "doc/*", "src/*", "CMakeLists.txt"

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin") # From bin to bin
        self.copy(pattern="*.dylib*", dst="lib", src="lib") 
        self.copy(pattern="*.so*", dst="lib", src="lib") 
       
    def build(self):
        cmake = CMake(self)
        cmake.definitions["LIBREALSENSE_FILE_LIBNAME"] = self.deps_user_info["librealsense"].realsense_file_library_name
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        pass
