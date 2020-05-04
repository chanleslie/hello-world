ABOUT ME
===========
The three (3) shell (.sh) scripts are here to serve as supplementary data to my capstone. They scripts were created and executed in Scripps Translational Research Institute's terminal.

ABSTRACT OF CAPSTONE
====================
In collaboration with American Heart Association, the Research Triangle Institute (RTI) International’s disease burden report projects 45% of the U.S. population to be affected by some cardiovascular disease (CVD) in 2035, costing the U.S. healthcare system approximately $318 billion to treat these heart conditions. CVD is influenced by both genetic and lifestyle factors, and it is commonly seen with conditions including atherosclerosis, high blood pressure, heart attacks, and heart failures. Despite the National Institutes of Health’s (NIH) $1.4 trillion funding for research and prevention programs of CVD, there is a continual rise of CVD prevalence. This suggests that a more effective preventative strategy is needed to take place. One of the proposed ways is through an absolute risk assessment based on an aggregate of estimated genetic risk across multiple chromosome loci -- a genetic risk score (GRS). Multiple research studies identified cytogenetic region 9p21 of the human genome to estimate an individual’s risk of inheriting a type of CVD called coronary artery disease (CAD). Hence, GRS can be useful in encouraging individuals to mitigate their risk by having a healthy diet and active lifestyle. An app, called MyGeneRank, is designed to generate a CAD GRS using an individual’s 23andMe genotype data. Unfortunately, there is an error with the GRS calculation; and it is discovered that the traditional statistical-based imputation, Minimac4, is giving rise to different GRS scores after multiple replications. To counteract the issues, a deep learning framework called the autoencoder is developed to accurately impute the genotype data with a faster processing time using a neural network. Prior results suggest that the autoencoder could replace Minimac4, especially when it comes to imputing on larger datasets where processing time becomes an issue. The current autoencoder code-script in the pipeline is hard-coded solely for chromosome 22. In other words, the autoencoder would have to be slightly re-coded for each of the other chromosomes. The objective of this study is to create an efficient imputation workflow by automating the imputation process across the whole genome so that it could be more effective and efficient than Minimac4 at imputing genotypes. 

PRE-PROCESSING STEP 
====================
The objective of this script is to extract the VMV (valley mountain valley) from HRC reference panel (one chromosome per run) by using the Positions and Minima files. It will set a VMV size threshold of 6000 variants. If the VMV block is larger than the maximum size threshold, then the script will look at the Minima file and slice the block using the minima information.

IMPUTATION STEP
=====================
The objective is to automate the process of generating imputed vcf files by parsing through the VMV files and impute the missing genetic variants. It will require 2 modules to be loaded into the environment: tensorflow/1.15.0py36-cuda & python/3.6.3. It will also need script "Imputation_inference_function_only_dosage.py". This can be shared by Scripps Translational Research Institute per their discretion. 

REQUIREMENTS
============
The user will need any version of a visual code editor (such as Spyder or Visual Studio Code) to view and edit the script. The scripts rely on some pre-existing files and script. These can be shared by Scripps Translatational Research Institute per their discretion. 


INSTALLATION INSTRUCTIONS
========================
There is no need for installation to view/edit the scripts. 

