/* a translation from Richard Single's awk programme */ 
 
#define NAME_LEN    12       /* 10 chars for allele name, plus colon and null */ 
#define LINE_LEN    132      /* RS changed from 120 to 132=6*2*(10+1) */ 
#define MAX_ROWS    500      /* RS changed from 1023 to 500 */
#define MAX_ALLELES 80 
#define MAX_LOCI    7 
#define MAX_COLS    MAX_LOCI * 2 
                             /* max genotypes:  2^max_loci*max_rows */ 
#define MAX_GENOS   20000    /* RS changed from 64*MAX_ROWS; 5000 in HAPLO */
#define MAX_HAPLOS  30000    /* RS added and changed declaration in main_proc; 1500 in HAPLO */
 
#define CRITERION   0.000001 
#define MAX_ITER    200      /* RS changed from 200 */
 
#define FALSE 0 
#define TRUE  1 
 
#define MAX_INIT 10 

#define MAX_GENOS_PER_PHENO 64 /* 2^(max_loci - 1) */

#define MAX_PERMU 1000
#define MAX_INIT_FOR_PERMU 10 

#ifdef EXTERNAL_MODE
#define FP_ITER fp_out
#define FP_PERMU fp_out
#else
#define FP_ITER NULL
#define FP_PERMU NULL
#endif

#define INIT_STATIC_DIM1(type,id,size1) \
memset(id, '\0', size1*sizeof(type))

#define INIT_STATIC_DIM2(type,id,size1,size2) \
memset(id, '\0', size1*size2*sizeof(type))

#define INIT_STATIC_DIM3(type,id,size1,size2,size3) \
memset(id, '\0', size1*size2*size3*sizeof(type))


