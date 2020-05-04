#!/bin/sh 
#=================================================
#Extractions Part A 
#=================================================
#This script is the automated pre-processing step to extract the VMV (valley mountain valley) from HRC reference panel 
#(one chromosome per run) by using the Positions and Minima files defined by Doug's method. It will set a VMV size 
#threshold of 6000 variants. If the VMV block is larger than the maximum size threshold, then the script will look at the 
#Minima file and slice the block using the minima information. If there are still large chunks remaining after 
#using the minima, then the script will slice these chunks to 6000 variants with 50% total overlap with neighboring blocks 

chr={1..22}
for i in $chr
do 
    bash make_extract_commands_by_var_limit.sh HRC.r1-1.EGA.GRCh37.chr${i}.MV_positions HRC.r1-1.EGA.GRCh37.chr${i}.MV_minima | tail -n 4
    echo "Done making $i folder!"
done
