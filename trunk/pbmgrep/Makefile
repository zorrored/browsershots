all : pbmgrep ppmfg

pbmgrep : pbmgrep.o Feature.o
	g++ -ggdb -o $@ -lnetpbm $^

ppmfg : ppmfg.o
	g++ -ggdb -o $@ -lnetpbm $<

%.o : %.cpp *.hpp
	g++ -ggdb -c $<
