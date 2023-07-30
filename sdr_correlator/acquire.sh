#! /bin/bash

device="0"
# freq="100000000"
freq="217800000"
srate="3200000"
gain="192"

./rtl2binary -d 0 -f "${freq}" -s "${srate}" -g "${gain}" &
./rtl2binary -d 1 -f "${freq}" -s "${srate}" -g "${gain}" &
