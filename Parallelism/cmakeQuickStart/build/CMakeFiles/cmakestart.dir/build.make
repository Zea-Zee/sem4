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
CMAKE_SOURCE_DIR = /home/zea/Desktop/Parallelism/cmakeQuickStart

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/zea/Desktop/Parallelism/cmakeQuickStart/build

# Include any dependencies generated for this target.
include CMakeFiles/cmakestart.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/cmakestart.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/cmakestart.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cmakestart.dir/flags.make

CMakeFiles/cmakestart.dir/main.cpp.o: CMakeFiles/cmakestart.dir/flags.make
CMakeFiles/cmakestart.dir/main.cpp.o: ../main.cpp
CMakeFiles/cmakestart.dir/main.cpp.o: CMakeFiles/cmakestart.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/zea/Desktop/Parallelism/cmakeQuickStart/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/cmakestart.dir/main.cpp.o"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/cmakestart.dir/main.cpp.o -MF CMakeFiles/cmakestart.dir/main.cpp.o.d -o CMakeFiles/cmakestart.dir/main.cpp.o -c /home/zea/Desktop/Parallelism/cmakeQuickStart/main.cpp

CMakeFiles/cmakestart.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cmakestart.dir/main.cpp.i"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/zea/Desktop/Parallelism/cmakeQuickStart/main.cpp > CMakeFiles/cmakestart.dir/main.cpp.i

CMakeFiles/cmakestart.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cmakestart.dir/main.cpp.s"
	/usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/zea/Desktop/Parallelism/cmakeQuickStart/main.cpp -o CMakeFiles/cmakestart.dir/main.cpp.s

# Object files for target cmakestart
cmakestart_OBJECTS = \
"CMakeFiles/cmakestart.dir/main.cpp.o"

# External object files for target cmakestart
cmakestart_EXTERNAL_OBJECTS =

cmakestart: CMakeFiles/cmakestart.dir/main.cpp.o
cmakestart: CMakeFiles/cmakestart.dir/build.make
cmakestart: CMakeFiles/cmakestart.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/zea/Desktop/Parallelism/cmakeQuickStart/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable cmakestart"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cmakestart.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/cmakestart.dir/build: cmakestart
.PHONY : CMakeFiles/cmakestart.dir/build

CMakeFiles/cmakestart.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cmakestart.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cmakestart.dir/clean

CMakeFiles/cmakestart.dir/depend:
	cd /home/zea/Desktop/Parallelism/cmakeQuickStart/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/zea/Desktop/Parallelism/cmakeQuickStart /home/zea/Desktop/Parallelism/cmakeQuickStart /home/zea/Desktop/Parallelism/cmakeQuickStart/build /home/zea/Desktop/Parallelism/cmakeQuickStart/build /home/zea/Desktop/Parallelism/cmakeQuickStart/build/CMakeFiles/cmakestart.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/cmakestart.dir/depend

