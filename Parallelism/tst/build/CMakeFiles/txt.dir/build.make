# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/zea/Desktop/Parallelism/tst

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/zea/Desktop/Parallelism/tst/build

# Include any dependencies generated for this target.
include CMakeFiles/txt.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/txt.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/txt.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/txt.dir/flags.make

CMakeFiles/txt.dir/hi.cpp.o: CMakeFiles/txt.dir/flags.make
CMakeFiles/txt.dir/hi.cpp.o: ../hi.cpp
CMakeFiles/txt.dir/hi.cpp.o: CMakeFiles/txt.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/zea/Desktop/Parallelism/tst/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/txt.dir/hi.cpp.o"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/txt.dir/hi.cpp.o -MF CMakeFiles/txt.dir/hi.cpp.o.d -o CMakeFiles/txt.dir/hi.cpp.o -c /home/zea/Desktop/Parallelism/tst/hi.cpp

CMakeFiles/txt.dir/hi.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/txt.dir/hi.cpp.i"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/zea/Desktop/Parallelism/tst/hi.cpp > CMakeFiles/txt.dir/hi.cpp.i

CMakeFiles/txt.dir/hi.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/txt.dir/hi.cpp.s"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/zea/Desktop/Parallelism/tst/hi.cpp -o CMakeFiles/txt.dir/hi.cpp.s

# Object files for target txt
txt_OBJECTS = \
"CMakeFiles/txt.dir/hi.cpp.o"

# External object files for target txt
txt_EXTERNAL_OBJECTS =

txt: CMakeFiles/txt.dir/hi.cpp.o
txt: CMakeFiles/txt.dir/build.make
txt: CMakeFiles/txt.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/zea/Desktop/Parallelism/tst/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable txt"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/txt.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/txt.dir/build: txt
.PHONY : CMakeFiles/txt.dir/build

CMakeFiles/txt.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/txt.dir/cmake_clean.cmake
.PHONY : CMakeFiles/txt.dir/clean

CMakeFiles/txt.dir/depend:
	cd /home/zea/Desktop/Parallelism/tst/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/zea/Desktop/Parallelism/tst /home/zea/Desktop/Parallelism/tst /home/zea/Desktop/Parallelism/tst/build /home/zea/Desktop/Parallelism/tst/build /home/zea/Desktop/Parallelism/tst/build/CMakeFiles/txt.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/txt.dir/depend

