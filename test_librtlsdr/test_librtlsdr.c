#include <stdio.h>
#include <rtl-sdr.h>
#include <unistd.h>
#include <assert.h>
#include <stdlib.h>

int main(void)
{
    fprintf(stdout, "Testing rtl-sdr library\n");
    uint32_t devcount, index;
    char manufact[256], product[256], serial[256];
    int res;
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
    fprintf(stdout, "Serial Number : %s\n", serial);

    return 0;
}
