#!/bin/bash
if [[ ${1} ]]; then
  btrfs subvolume list ${1} | grep -v container
else
  echo "pls provide path to btrfs root mount point"
  echo "try '/'":
  btrfs subvolume list / | grep -v container
fi


