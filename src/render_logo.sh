#!/bin/bash

target_file="$1"
output_file="$1"

logo_file="../static/krebs_plain2.png"
geometry="+200+200"

composite -geometry $geometry $target_file $logo_file $output_file
