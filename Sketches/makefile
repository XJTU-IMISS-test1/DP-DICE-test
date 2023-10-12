datasets_prepare: MurmurHash3.o datasets.o
	g++ -o datasets_prepare datasets.o MurmurHash3.o -pthread
gene: MurmurHash3.o gene_sketch.o
	g++ -o gene gene_sketch.o MurmurHash3.o -pthread