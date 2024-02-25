/* $Author: schaid $ */
/* $Date: 2007/02/27 20:18:01 $ */
/* $Header: /projects/genetics/cvs/cvsroot/haplo.stats/src/haplo_em_pin.h,v 1.7 2007/02/27 20:18:01 schaid Exp $ */
/* $Locker:  $ */

/*
*License: 
*
*Copyright 2003 Mayo Foundation for Medical Education and Research. 
*
*This program is free software; you can redistribute it and/or modify it under the terms of 
*the GNU General Public License as published by the Free Software Foundation; either 
*version 2 of the License, or (at your option) any later version.
*
*This program is distributed in the hope that it will be useful, but WITHOUT ANY 
*WARRANTY; without even the implied warranty of MERCHANTABILITY or 
*FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for 
*more details.
*
*You should have received a copy of the GNU General Public License along with this 
*program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, 
*Boston, MA 02111-1307 USA
*
*For other licensing arrangements, please contact Daniel J. Schaid.
*
*Daniel J. Schaid, Ph.D.
*Division of Biostatistics
*Harwick Building û Room 775
*Mayo Clinic
*200 First St., SW
*Rochester, MN 55905
*
*phone: 507-284-0639
*fax:      507-284-9542
*email: schaid@mayo.edu 
*/

#define R_chk_calloc calloc
#define R_chk_realloc realloc
#define R_chk_free free
#define REprintf printf
#define Rf_error error


typedef struct HAP_T {
  int id;
  int code;
  int pair_id;
  int keep;
  int *loci;
  double post, wt;
} HAP;


typedef struct HAPUNIQUE_T {
  int code;
  int keep;
  int *loci;
  double prior;
} HAPUNIQUE;

static int iminarg1, iminarg2;

# define imin(a,b) (iminarg1=(a), iminarg2=(b), \
		    (iminarg1) < (iminarg2) ? (iminarg1) : (iminarg2) )

/* Windows compatibility */

#ifdef _WINDOWS
#define CDECL __cdecl
#else
#define CDECL
#endif


/************************** Function prototypes ***********************************/

static HAP* new_hap(int id, int pair_id, double wt, double prior, double post);

static void write_hap_list(HAP** so, int n_hap);


static int CDECL cmp_hap(const void *to_one, const void *to_two);

static int CDECL cmp_subId_hapPairId(const void *to_one, const void *to_two);

static int CDECL cmp_hap_code(const void *to_one, const void *to_two);

static int code_haps(int n_hap, HAP **hap_list);

static int hap_enum(HAP ***hap_list_ptr, double **prior_ptr, int *max_haps, int *n_alleles, int insert_loc, 
		     int n_hap, int *pair_id);

static HAP* copy_hap(HAP *old);

static int num_het(HAP* h1,HAP* h2);

static void hap_prior(int n_hap, HAP** hap_list, double *prior, int n_u_hap,
                      double min_prior);

static int hap_posterior(int n_hap, HAP **hap_list, double *prior, 
			  int n_u_hap, double min_posterior, double *lnlike);

static int **int_vec_to_mat(int *Yvec, int nrow, int ncol);

static int **int_matrix(int nrow, int ncol);

static void set_posterior(int n_hap, HAP **hap_list, int *random_start);

static int ranAS183_seed(int iseed1, int iseed2, int iseed3);

static double ranAS183(void);

static void errmsg(char *string);

static HAPUNIQUE* copy_hap_unique(HAP *old, double *prior);

static void unique_haps(int n_hap, HAP **hap_list, HAPUNIQUE **u_hap_list, double *prior);

static int count_unique_haps(int n_hap, HAP **hap_list);

static void write_prior(int n, double *prior);

static void write_unique_hap_list(HAPUNIQUE** so, int n_hap);

static void divideKeep(HAP **hap_list, int n, int *nReturn);

static void add_more_memory(HAP ***hap_list, double **prior,int *max_haps);

static void insert_new_hap_pair(HAP ***hap_list_ptr, double **prior_ptr, 
                                int *max_haps, int insert_loc,
                                HAP *h1_old, HAP *h2_old, 
                                int a1_new, int a2_new,
                                int *pair_id, int *j);

static void overwrite_hap(HAP *new, HAP *old);

void checkIntMax(int *intMax);
