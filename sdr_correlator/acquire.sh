#! /bin/bash

device="0"
# freq="100000000"
freq="97700000"
srate="2000000"
gain="192"

./rtl2binary -d 0 -f "${freq}" -s "${srate}" -g "${gain}"
# (./rtl2binary2 &)
