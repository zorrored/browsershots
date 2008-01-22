# CPPFLAGS=-ggdb
CPPFLAGS=-O3

all : pbmgrep ppmfg

pbmgrep : pbmgrep.o Feature.o
	g++ $(CPPFLAGS) -o $@ -lnetpbm $^
	strip $@

ppmfg : ppmfg.o
	g++ $(CPPFLAGS) -o $@ -lnetpbm $<
	strip $@

%.o : %.cpp *.hpp
	g++ $(CPPFLAGS) -c $<

install :
	cp -f ppmfg pbmgrep /usr/local/bin
