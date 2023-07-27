#include <stdio.h>
#include <rtl-sdr.h>
#include <unistd.h>
#include <assert.h>
#include <stdlib.h>
#include <time.h>
#include "sdrbuffer.h"

int main(void)
{
    uint32_t devcount, index, setfreq, setrate;
    char manufact[256], product[256], serial[256];
    int res, nread;
    static rtlsdr_dev_t *dev = NULL;
    struct sdrbuf rtlbuffer;
    struct timespec acqtime;

    index = 0;

    devcount = rtlsdr_get_device_count();
    if (devcount<1)
    {
        fprintf(stderr, "No devices found ! Exiting ....\n");
        exit(EXIT_FAILURE);
    }
    fprintf(stdout, "Found %d device(s)\n", devcount);
    res = rtlsdr_get_device_usb_strings(index, manufact, product, serial);
    assert(res==0);

    fprintf(stdout, "Manufacturer : %s\n", manufact);
    fprintf(stdout, "Product : %s\n", product);
    fprintf(stdout, "Serial Number in ASCII : %s\n", serial);

    rtlbuffer.serial_no = (uint32_t) strtol(serial, NULL, 10);
    fprintf(stdout, "Serial Number in numerical : %d\n", rtlbuffer.serial_no );

    res = rtlsdr_open(&dev, index);
    assert(res==0);

    setrate = 2000000;
    res = rtlsdr_set_sample_rate(dev, setrate);
    assert(res==0);
    rtlbuffer.srate = rtlsdr_get_sample_rate(dev);
    fprintf(stdout, "Sample rate achieved is %d\n",  rtlbuffer.srate);

    setfreq = 97700000; //ABC Classic !
    res = rtlsdr_set_center_freq(dev, setfreq);
    assert(res==0);
    rtlbuffer.cfreq = rtlsdr_get_center_freq(dev);
    fprintf(stdout, "Tuned to %d\n", rtlbuffer.cfreq);
 
    res = rtlsdr_reset_buffer(dev);
    usleep(5000);
    uint8_t dummybuffer[262144];
    res = rtlsdr_read_sync(dev, dummybuffer, 262144, &nread); // Dummy read    
    if (nread != 262144) 
    {
        fprintf(stderr, "Error, can't read reliably.\n");
        return -1; // Not the best way to quit
    }

    res = rtlsdr_reset_buffer(dev);
    assert(res==0);
    nread = BLOCKSIZE;

    res = clock_gettime(CLOCK_REALTIME, &acqtime);
    assert(res==0);

    rtlbuffer.tv_sec  = (uint32_t)acqtime.tv_sec;
    rtlbuffer.tv_nsec = (uint32_t)acqtime.tv_nsec;
    res = rtlsdr_read_sync(dev, rtlbuffer.buffer, BLOCKSIZE, &nread);
    assert(res==0);

    fprintf(stdout, "Acquired data at %d seconds and %d nsecs \n",  rtlbuffer.tv_sec,  rtlbuffer.tv_nsec);
    rtlsdr_close(dev);

    fprintf(stdout, "Writing data into a binary file \n");

    FILE * binfile= fopen("rtldata.bin", "wb");
    if (binfile != NULL) 
    {
        // fwrite(&rtlbuffer, sizeof(struct sdrbuf), 1, binfile); // original
        fwrite(&rtlbuffer, sizeof(rtlbuffer), 1, binfile); // seems to work ?
        fclose(binfile);
    }

    fprintf(stdout, "Exiting ! \n");

    return 0;
}
