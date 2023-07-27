all: rtl2binary

rtl2binary: rtl2binary.c
	@echo "Compiling rtl2binary"
	gcc -Wall rtl2binary.c -o rtl2binary -lrtlsdr -lrt

clean : 
	rm rtl2binary