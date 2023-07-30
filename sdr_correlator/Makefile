.PHONY: sdrbuffer.h

all: rtl2binary

rtl2binary: rtl2binary.c
	@echo "Compiling rtl2binary"
	gcc -O0 -Wall rtl2binary.c -o rtl2binary -lrt -lrtlsdr

clean : 
	rm -f rtl2binary
