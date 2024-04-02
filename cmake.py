import os
import subprocess

LIBRARIES = {
    "sfml": {
        "components": ["graphics", "audio"],
        "version": "2.5",
        "dir": ""
    },
    "sdl2": {  
        "components": ["SDL2"],
        "version": "2.0.12",
        "dir": ""  
    }
}

def copy_dll(lib):
    if lib.lower() == "sdl2":
        dll_path = input(f"Enter the path for {lib.upper()}.dll: ")
        dll_path = dll_path.replace("\\", "/") 
        os.system(f'copy {dll_path} {os.getcwd()}')

def generate_sfml_cmake(lib_info, lib, project_name, cpp_file):
    cmake_content = f"""
    cmake_minimum_required(VERSION 3.10)
    project({project_name})

    set({lib.upper()}_DIR "{lib_info["dir"]}")
    find_package({lib.upper()} {lib_info["version"]} COMPONENTS {" ".join(lib_info["components"])} REQUIRED)

    add_executable({project_name} {cpp_file})
    target_link_libraries({project_name} {lib.lower()}-graphics {lib.lower()}-audio)
    """
    return cmake_content


def generate_sdl_cmake(lib_info, lib, project_name, cpp_file):
    sdl_include_dir = input("Enter the SDL2 include directory(include): ").replace("\\", "/")
    sdl_library_dir = input("Enter the SDL2 library directory(lib): ").replace("\\", "/")
    sdl_library_dir += "/libSDL2.dll.a"

    cmakelist_content = f"""
    cmake_minimum_required(VERSION 3.10)
    project({project_name})

    set(CMAKE_CXX_STANDARD 14)

    # Add your source files here
    set(SOURCE_FILES {cpp_file})

    # SDL2 paths
    set(SDL2_INCLUDE_DIR "{sdl_include_dir}")
    set(SDL2_LIBRARY "{sdl_library_dir}")

    # SDL2
    find_package(SDL2 REQUIRED)
    include_directories(${{SDL2_INCLUDE_DIR}})

    add_executable({project_name} ${{SOURCE_FILES}})
    target_link_libraries({project_name} ${{SDL2_LIBRARY}})
    """
    return cmakelist_content

def main():
    print("Welcome to the CMake configuration script!")
    project_name = input("Enter the project name: ")
    cpp_file = input("Enter the name of your cpp/c file: ")
    libraries = input("Enter the library (e.g., sfml sdl2): ").split()

    try:
        for lib in libraries:
            copy_dll(lib)
            lib_info = LIBRARIES.get(lib)
            if not lib_info:
                raise ValueError(f"Library {lib} is not defined.")
            if not lib_info["dir"]:
                lib_info["dir"] = input(f"Enter the directory for {lib}: ")
            lib_info["dir"] = lib_info["dir"].replace("\\", "/")  # Convert backslashes to forward slashes
            if lib.lower() == "sfml":
                cmake_content = generate_sfml_cmake(lib_info, lib, project_name, cpp_file)
            elif lib.lower() == "sdl2":
                cmake_content = generate_sdl_cmake(lib_info, lib, project_name, cpp_file)
            with open("CMakeLists.txt", "w") as cmake_file:
                cmake_file.write(cmake_content)
        print("CMake configuration written to CMakeLists.txt successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
