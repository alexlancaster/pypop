### haplo.em

This is the beginning of a wrapping the EM haplotype algorithm from the R package 'haplo.stats'.

To compile as standalone use the following:

     gcc -DMATHLIB_STANDALONE=1 -I../pval haplo_em_pin.c -o haplo_em_pin -lm

RS added a main() function with a hard coded example from the haplo.stats R doc. 
It passes the geno_vec containing genotypes correctly, but other pointers are not being handled correctly and give a segfault. 
There are comments '//RS commented' and additions '//RS added' flagged in the code along with some print statements to see


