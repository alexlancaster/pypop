/* a translation from Richard Single's awk programme */ 
 
#define NAME_LEN    12       /* 10 chars for allele name, plus colon and null */ 
#define LINE_LEN    132      /* RS changed from 120 to 132=6*2*(10+1) */ 
#define MAX_ROWS    500      /* RS changed from 1023 to 500 */
#define MAX_ALLELES 80 
#define MAX_LOCI    6 
#define MAX_COLS    MAX_LOCI * 2 
                             /* max genotypes:  2^max_loci*max_rows */ 
#define MAX_GENOS   20000    /* RS changed from 64*MAX_ROWS; 5000 in HAPLO */
#define MAX_HAPLOS  30000    /* RS added and changed declaration in main_proc; 1500 in HAPLO */
 
#define CRITERION   0.000001 
#define MAX_ITER    100      /* RS changed from 200 */
 
#define FALSE 0 
#define TRUE  1 
 
