### haplo.em

This is the beginning of a wrapping the EM haplotype algorithm from the R package 'haplo.stats'.

To compile as standalone use the following:

     gcc -DMATHLIB_STANDALONE=1 -I../pval haplo_em_pin.c -o haplo_em_pin -lm

This includes a main() function with a hard coded example from the haplo.stats R doc. 


