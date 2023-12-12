#!/bin/bash

for i in {1..1}
do
    ./stamp-test.sh real_polka_1.stm stm real 1
    ./stamp-test.sh real_polka_2.stm stm real 2
    ./stamp-test.sh real_polka_4.stm stm real 4
    ./stamp-test.sh real_polka_8.stm stm real 8
    ./stamp-test.sh real_polka_16.stm stm real 16
done

