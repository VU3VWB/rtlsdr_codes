.PHONY: sdrbuffer.h

all: rtl2binary1 rtl2binary2

rtl2binary1: rtl2binary1.c
	@echo "Compiling rtl2binary1"
	gcc -Wall rtl2binary1.c -o rtl2binary1 -lrtlsdr -lrt

rtl2binary2: rtl2binary2.c
	@echo "Compiling rtl2binary2"
	gcc -Wall rtl2binary2.c -o rtl2binary2 -lrtlsdr -lrt

clean : 
	rm -f rtl2binary1 rtl2binary2