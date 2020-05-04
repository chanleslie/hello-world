#!/bin/bash

#=====================================================
#Post-Processing Script 
#=====================================================
#The objective is to automate the process of generating imputed vcf files. More specifically, You will need to: 
# 1. Go through every file in a folder via for-loop through files in a directory 
# 2. To extract the filename and only obtain the "chop-coordinates" aka "coordinates"
# 3. Use these coordinates as variables to change nomenclature 
# 4. Run "Imputation_inference_function_only_dosage.py" for that coordinates 
# 5. Repeat for remainder of the files in that directory with changing coordinates

module load tensorflow/1.15.0py36-cuda #This is the GPU version module
module load python/3.6.3 #To load python to my environment 

working_path='/gpfs/group/torkamani/lchan'
reference='/mnt/stsi/stsi0/raqueld/1KG_VMV/1000G_chr22_positions'
genotype_array='/mnt/stsi/stsi0/lchan/decompressed_genotype'
model='/mnt/stsi/stsi0/raqueld/1KG_VMV/1000G_chr22_models'
output='/mnt/stsi/stsi0/lchan/wrapper_output'
cd ${working_path}
for f in ${genotype_array}/*.VMV1.masked; do
    prefix=$(echo $f | sed -e 's/\.masked//g') #This simply removed the word ".masked". sed simply replaces a string. The string starts with 1000G. 
    prefix2=$(basename $prefix | sed 's/1000G/HRC.r1-1.EGA/g') #The string starts with HRC. 
    pos=$(basename $prefix2 | awk -v dir="${reference}" '{print dir "/" $0 ".000.1-5"}') #You have to call out the basename. If not, the command won't know what file I'm specifically. $0 means the whole line of argument aka itself aka "basename of $prefix"
    masked=$f
    model_f=$(basename $prefix2 | awk -v dir="${model}" '{print dir "/" $0 "_model"}')
    output_f=$(basename $prefix | awk -v dir="${output}" '{print dir "/" $0 ".masked.autoencoder_imputed_round1.vcf"}')
    python3 ${working_path}/Imputation_inference_function_only_dosage.py $pos $masked $model_f $output_f"    
done