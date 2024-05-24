CXX=pgc++
CXXFLAGS=-fast -acc -ta=tesla -Minfo=accel \
         -I/opt/nvidia/hpc_sdk/Linux_x86_64/23.11/math_libs/12.3/targets/x86_64-linux/include \
         -I/opt/nvidia/hpc_sdk/Linux_x86_64/23.11/cuda/12.3/include \
         -lboost_program_options
LDFLAGS=-L/opt/nvidia/hpc_sdk/Linux_x86_64/23.11/math_libs/12.3/targets/x86_64-linux/lib \
        -L/opt/nvidia/hpc_sdk/Linux_x86_64/23.11/cuda/12.3/lib64 \
        -lcublas -lcudart

# Список исходных файлов и объектных файлов
SRCS = laplace2d.cpp jacobi.cpp
OBJS = $(SRCS:.cpp=.o)
EXEC = gpu_ver

# Цель по умолчанию
all: $(EXEC) run

# Правило для сборки исполняемого файла
$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS) $(NVTXLIB)
	@$(MAKE) clean_obj

# Правило для запуска программы с аргументами
run: $(EXEC)
	export CUDA_VISIBLE_DEVICES=1
	./$(EXEC) --NX 128 --NY 128

# Правило для очистки объектных файлов
.PHONY: clean clean_obj
clean:
	-rm -f $(OBJS) $(EXEC)

clean_obj:
	-rm -f $(OBJS)

# Правило для сборки объектных файлов
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $< $(NVTXLIB)
