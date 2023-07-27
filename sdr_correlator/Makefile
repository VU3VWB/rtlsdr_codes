.PHONY: sdrbuffer.h

all: rtl2binary read_rtlbinary

rtl2binary: rtl2binary.c
	@echo "Compiling rtl2binary"
	gcc -Wall rtl2binary.c -o rtl2binary -lrtlsdr -lrt

read_rtlbinary: read_rtlbinary.c
	@echo "Compiling code to read the binary file"
	gcc -Wall read_rtlbinary.c -o read_rtlbinary -lrt

clean : 
	rm -f rtl2binary read_rtlbinary