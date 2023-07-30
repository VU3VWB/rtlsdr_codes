#! /bin/bash

# freq="97000000"
freq="217800000"
# freq="117800000"

srate="2400000"
gain="192"

./rtl2binary -d 0 -f "${freq}" -s "${srate}" -g "${gain}" &
./rtl2binary -d 1 -f "${freq}" -s "${srate}" -g "${gain}" &

wait