#!/bin/sh 
#=================================================
#Extractions Part B 
#=================================================

for i in {'3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21'}
do 
    cd /gpfs/home/lchan/VMV_VCF_Extractions/chr${i}
    chmod 755 *.sh
    bash extract_vcf_6000_variants.sh
    bash extract_vcf_too_many_VMV1_variants.sh
    echo "Done extracting VCF for chr${i}"
done
