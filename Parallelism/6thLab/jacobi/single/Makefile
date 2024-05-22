# Компилятор и флаги
CXX = pgc++
CXXFLAGS = -Minfo=all -acc -ta=
LDFLAGS = -lboost_program_options
NVTXLIB = -I/opt/nvidia/hpc_sdk/Linux_x86_64/23.11/cuda/12.3/include/

# Список исходных файлов и объектных файлов
SRCS = laplace2d.cpp jacobi.cpp
OBJS = $(SRCS:.cpp=.o)
EXEC = single_ver

# Цель по умолчанию
all: $(EXEC) run

# Правило для сборки исполняемого файла
$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS) $(NVTXLIB)
	@$(MAKE) clean_obj

# Правило для запуска программы с аргументами
run: $(EXEC)
	./$(EXEC) --NX 128 --NY 128
	./$(EXEC) --NX 256 --NY 256
	./$(EXEC) --NX 512 --NY 512
	./$(EXEC) --NX 1024 --NY 1024

# Правило для очистки объектных файлов
.PHONY: clean clean_obj
clean:
	-rm -f $(OBJS) $(EXEC)

clean_obj:
	-rm -f $(OBJS)

# Правило для сборки объектных файлов
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $< $(NVTXLIB)
