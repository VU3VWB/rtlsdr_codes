#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <assert.h>
#include <time.h>
#include <rtl-sdr.h>
#include "sdrbuffer.h"
#define DUMMYBYTES 262144

int main(int argc, char **argv)
{
    uint32_t devcount, index, setfreq, setrate;
    char manufact[256], product[256], serial[256], c;
    int res, nread;
    static rtlsdr_dev_t *dev = NULL;
    struct sdrbuf *rtlbuffer = malloc(sizeof(struct sdrbuf));
    struct timespec acqtime;

    index = 0; //default

    while ((c = getopt (argc, argv, "-d:")) != -1)
    {
        switch (c)
        {
            case 'd':
                index = (uint32_t) strtol(optarg, NULL, 10);
                break;
            case '?':
                fprintf(stderr, "Inaccurate arguments, exiting ....\n");
                exit(EXIT_FAILURE);
            default:
                abort ();
        }
    }

    devcount = rtlsdr_get_device_count();
    if (devcount<1)
    {
        fprintf(stderr, "No devices found ! Exiting ....\n");
        exit(EXIT_FAILURE);
    }
    fprintf(stdout, "Found %d device(s) and attempting to open device indexed %d\n", devcount, index);

    res = rtlsdr_open(&dev, index);
    if (res != 0)
    {
        fprintf(stderr, "The selected device could not be opened ! Exiting ....\n");
        exit(EXIT_FAILURE);
    }

    res = rtlsdr_get_device_usb_strings(index, manufact, product, serial);
    rtlbuffer->serial_no = (uint32_t) strtol(serial, NULL, 10);
    fprintf(stdout, "Manufacturer : %s\n", manufact);
    fprintf(stdout, "Product : %s\n", product);
    // fprintf(stdout, "Serial Number in ASCII : %s\n", serial);
    fprintf(stdout, "Device serial Number is : %d\n", rtlbuffer->serial_no);

    setrate = 2000000;
    res = rtlsdr_set_sample_rate(dev, setrate);
    assert(res==0);
    rtlbuffer->srate = rtlsdr_get_sample_rate(dev);
    fprintf(stdout, "Sample rate achieved is %d\n",  rtlbuffer->srate);

    setfreq = 97700000; //ABC Classic !
    res = rtlsdr_set_center_freq(dev, setfreq);
    assert(res==0);
    rtlbuffer->cfreq = rtlsdr_get_center_freq(dev);
    fprintf(stdout, "Tuned to %d\n", rtlbuffer->cfreq);

    res = rtlsdr_reset_buffer(dev);
    usleep(5000);
    uint8_t dummybuffer[DUMMYBYTES];
    res = rtlsdr_read_sync(dev, dummybuffer, DUMMYBYTES, &nread); // Dummy read    
    if (nread != DUMMYBYTES) 
    {
        fprintf(stderr, "Error, can't read reliably.\n");
        exit(EXIT_FAILURE);
    }

    res = rtlsdr_reset_buffer(dev);
    assert(res==0);

    res = clock_gettime(CLOCK_REALTIME, &acqtime);
    assert(res==0);

    rtlbuffer->bufsize = (uint32_t) BUFSIZE;

    rtlbuffer->tv_sec  = (uint32_t)acqtime.tv_sec;
    rtlbuffer->tv_nsec = (uint32_t)acqtime.tv_nsec;

    for (int i=0; i < (int)(BUFSIZE/BLOCKSIZE); i++)
    {
        res = rtlsdr_read_sync(dev, (rtlbuffer->buffer + (i*BLOCKSIZE)), BLOCKSIZE, &nread);
        // assert(res==0);
    }

    fprintf(stdout, "Acquired data at %d seconds and %d nsecs \n",  rtlbuffer->tv_sec,  rtlbuffer->tv_nsec);
    rtlsdr_close(dev);

    fprintf(stdout, "Writing data into a binary file \n");

    FILE * binfile= fopen("rtldata.bin", "wb");
    if (binfile != NULL) 
    {
        // fwrite(&rtlbuffer, sizeof(struct sdrbuf), 1, binfile); // original
        fwrite(rtlbuffer, sizeof(struct sdrbuf), 1, binfile); 
        fclose(binfile);
    }

    fprintf(stdout, "Exiting ! \n");

    return 0;
}
