#!/bin/bash
rm pypop.img
singularity create --size 3000 pypop.img
sudo singularity bootstrap pypop.img Singularity
