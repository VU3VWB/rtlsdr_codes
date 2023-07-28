#! /bin/bash

device="0"
# freq="100000000"
freq="145000000"
# srate="2000000"
srate="3200000"
gain="192"

./rtl2binary -d 0 -f "${freq}" -s "${srate}" -g "${gain}"
# (./rtl2binary2 &)
