CC=gcc
CFLAGS=-std=c11 -Wall -O2 -fopenmp
LDFLAGS=-lm -fopenmp
EXEC=integral

all: $(EXEC)

$(EXEC): integral.o
	$(CC) -o $@ $^ $(LDFLAGS)

integral.o: integral.c
	$(CC) -o $@ -c $< $(CFLAGS)

clean:
	rm -f *.o $(EXEC)
