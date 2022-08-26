#!/bin/bash

read -p "What domain? " domain

my_array=$(host -t ns $domain | cut -d " " -f 4 | sed 's/.$//')

for address in $my_array;
do
    zone= host -l $domain $address;
    echo $zone;
done
