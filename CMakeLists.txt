cmake_minimum_required(VERSION 3.13)
project(ISMRMRD VERSION 1.14.2 LANGUAGES C CXX)

# 设置 CMake 模块路径
set(ISMRMRD_CMAKE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
list(APPEND CMAKE_MODULE_PATH "${ISMRMRD_CMAKE_DIR}")

# 选项配置
option(USE_HDF5_DATASET_SUPPORT "Enable HDF5 dataset support" ON)
option(BUILD_TESTS "Build unit tests" OFF)
option(BUILD_UTILITIES "Build utilities" OFF)
option(BUILD_EXAMPLES "Build examples" OFF)

# 设置默认编译类型
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type (Debug, Release, etc.)" FORCE)
endif()

# 设置默认 C++ 标准
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 包含目录
set(ISMRMRD_INCLUDE_DIRS
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# 设置 schema 路径
set(ISMRMRD_SCHEMA_DIR "${CMAKE_CURRENT_SOURCE_DIR}/schema")
set(ISMRMRD_XML_SCHEMA "${ISMRMRD_SCHEMA_DIR}/ismrmrd.xsd")
file(READ "${ISMRMRD_XML_SCHEMA}" SCHEMA_CONTENT)
string(REPLACE "\n" "" SCHEMA_CONTENT "${SCHEMA_CONTENT}")
string(SHA1 SCHEMA_HASH "${SCHEMA_CONTENT}")

# 检查 schema 文件的一致性
set(EXPECTED_SCHEMA_HASH "40036f175a77542b50acbcfb0f019094c90b5e18")
# if(NOT SCHEMA_HASH STREQUAL EXPECTED_SCHEMA_HASH)
#     message(FATAL_ERROR "Schema file hash mismatch! Expected: ${EXPECTED_SCHEMA_HASH}, but got: ${SCHEMA_HASH}.")
# endif()

# 查找依赖
find_package(PugiXML REQUIRED)

if(USE_HDF5_DATASET_SUPPORT)
    find_package(HDF5 REQUIRED COMPONENTS C)
    set(ISMRMRD_HDF5_LIBS HDF5::HDF5)
else()
    message(WARNING "HDF5 support is disabled. Dataset functionality will not be available.")
    set(ISMRMRD_HDF5_LIBS "")
endif()

# 定义主库
add_library(ismrmrd SHARED
    libsrc/ismrmrd.c
    libsrc/ismrmrd.cpp
    libsrc/xml.cpp
    libsrc/meta.cpp
    libsrc/serialization.cpp
    libsrc/waveform.cpp
    libsrc/waveform.c
)
target_include_directories(ismrmrd PUBLIC ${ISMRMRD_INCLUDE_DIRS})
target_link_libraries(ismrmrd PUBLIC pugixml::pugixml ${ISMRMRD_HDF5_LIBS})
set_target_properties(ismrmrd PROPERTIES VERSION ${PROJECT_VERSION} SOVERSION ${PROJECT_VERSION_MAJOR})

# 安装目标
install(TARGETS ismrmrd EXPORT ISMRMRDTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)
install(DIRECTORY include/ DESTINATION include )
install(FILES "${ISMRMRD_XML_SCHEMA}" DESTINATION share/ismrmrd/schema)

# CMake 包配置
include(CMakePackageConfigHelpers)
write_basic_package_version_file("${CMAKE_BINARY_DIR}/ISMRMRDConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)
install(EXPORT ISMRMRDTargets
    FILE ISMRMRDTargets.cmake
    DESTINATION lib/cmake/ISMRMRD
)
configure_file(cmake/ISMRMRDConfig.cmake.in
    "${CMAKE_BINARY_DIR}/ISMRMRDConfig.cmake"
    @ONLY
)
install(FILES
    "${CMAKE_BINARY_DIR}/ISMRMRDConfig.cmake"
    "${CMAKE_BINARY_DIR}/ISMRMRDConfigVersion.cmake"
    DESTINATION lib/cmake/ISMRMRD
)

# 测试和示例
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
