#!/bin/bash
if [[ ${1} ]]; then
    mkdir "${1}"
    mount /dev/mapper/system -o subvolid=256 "${1}"
    sleep 1
    mount /dev/mapper/system -o subvolid=257 "${1}"/home
    mount /dev/mapper/system -o subvolid=258 "${1}"/var/log
    mount /dev/mapper/system -o subvolid=259 "${1}"/var/cache/pacman/pkg
else
    echo "pls provide path to btrfs root mount point"
fi



