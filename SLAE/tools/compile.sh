#!/bin/bash

nasm -f elf32 -o $1.o $1.asm
ld -o $1 $1.o -z execstack -N

echo 'Done'
