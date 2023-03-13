all: test_librtlsdr

test_librtlsdr: test_librtlsdr.c
	@echo "Compiling test rtl-sdr"
	gcc -Wall test_librtlsdr.c -o test_librtlsdr -lrtlsdr
clean : 
	rm test_librtlsdr