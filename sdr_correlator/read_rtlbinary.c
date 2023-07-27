#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <stdlib.h>
#include "sdrbuffer.h"

int main(void)
{

    struct sdrbuf rtlbuffer;
    fprintf(stdout, "Reading the binary file \n");

    FILE * binfile= fopen("rtldata.bin", "rb");
    if (binfile != NULL) 
    {
        fread(&rtlbuffer, sizeof(struct sdrbuf), 1, binfile);
        fclose(binfile);
    }

    fprintf(stdout, "Data acquired at %d seconds and %d nsecs \n",  rtlbuffer.tv_sec,  rtlbuffer.tv_nsec);
    fprintf(stdout, "Serial Number was : %d\n", rtlbuffer.serial_no );
    fprintf(stdout, "Was tuned to %d\n", rtlbuffer.cfreq);
    fprintf(stdout, "Sample rate achieved was %d\n",  rtlbuffer.srate);

    return 0;
}