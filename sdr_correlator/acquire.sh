#! /bin/bash

device="0"
freq="100000000"
srate="2000000"
gain="192"

./rtl2binary -d "${device}" -f "${freq}" -s "${srate}" -g "${gain}"
# (./rtl2binary2 &)
