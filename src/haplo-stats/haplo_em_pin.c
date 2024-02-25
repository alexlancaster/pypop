/* $Author: sinnwell $ */
/* $Date: 2013/01/14 19:10:42 $ 
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
*Harwick Building Room 775
*Mayo Clinic
*200 First St., SW
*Rochester, MN 55905
*
*phone: 507-284-0639
*fax:      507-284-9542
*email: schaid@@@@mayo.edu 
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <limits.h>
//#include <R.h>  
#include <Rmath.h>
#include <nmath.h>
#include "haplo_em_pin.h"

/* Progressive insertion of loci into haplotypes with EM algorithm */

/*************** Global vars ******************************************************/

static int n_loci, *loci_used;               /* used for qsort functions         */   
static HAP **ret_hap_list;                    /* stored for later return to S+    */
static HAPUNIQUE **ret_u_hap_list;
static int ret_n_hap, ret_n_u_hap, ret_max_haps;

/**********************************************************************************/

void haplo_em_pin(
   int    *S_n_loci,             /* number of loci                                 */
   int    *n_subject,            /* number of subjects                             */
   double  *weight,               /* weight per subject                             */
   int    *geno_vec,             /* vector of genotypes,  col-major from           */
                                  /* n_subject x 2*n_loci matrix                    */
   int    *n_alleles,            /* vector of number alleles per locus,            */
				  /* length=n_loci                                  */
   int    *max_haps,             /* number of maximum haplotypes over all subjects */
				  /*  - CRITICAL for memory alloc                   */
   int    *max_iter,             /* max num. iters for each EM loop                */
   int    *loci_insert_order,    /* vector for order of insert of loci for         */
                                  /* progressive insertion; length = n_loci         */
   double  *min_prior,            /* trim haplo's with prior < min_prior            */
   double  *min_posterior,        /* trim subject's pair of haplos if               */
				  /* post < min_posterior                           */
   double  *tol,                  /* convergence tolerance for change in lnlike in  */ 
				  /*  EM loop                                       */
   int    *insert_batch_size,    /* number of loci to insert in a batch before     */
                                  /*  each EM loop; order of inserted               */
                                  /* loci determined by loci_insert_order           */
   int    *converge,             /* convergence indicator for EM                   */
   double  *S_lnlike,             /* lnlike from final EM                           */
   int    *S_n_u_hap,            /* number of unique haplotypes                    */
   int    *n_hap_pairs,          /* total number of pairs of haplotypes over all   */
                                  /* subjects                                       */
   int    *random_start,         /* indicator of random posteriors should be       */
				  /* generated at the start of each EM loop.        */
                                  /* 1 = Yes, 0 = No                                */
   int    *iseed1,               /* seeds for AS183 random unif                    */
   int    *iseed2,	
   int    *iseed3,
   int    *verbose)              /* indicator if verbose pringing during  run,     */
                                  /* for debugging. verbose=0 means no printing     */
                                  /* verbose=1 means lots of printing to screen     */
{


  int i, j, k, iter, n_iter, insert_loc;
  int is, ie, n_batch;
  int n_u_hap, n_hap, n_trim, pair_id, len_hap_list, indx1, indx2;
  int **geno;
  double lnlike, lnlike_old;
  double *prior;

  HAP **hap_list;     /* List of all haplotypes = array of pointers to hap structs */
  HAPUNIQUE **u_hap_list;   /* List of unique haplotypes */

  /* convert from S vecs to  C structures */

  n_loci = *S_n_loci;
  geno = int_vec_to_mat(geno_vec, *n_subject, 2*n_loci);


  if(*verbose){
    REprintf("geno matrix:\n");
    for(i=0;i< *n_subject;i++){
      for (j=0; j< (2*n_loci); j++) {
        REprintf("%i ",geno[i][j]);
      }
      REprintf("\n");
    }
  }

  prior = (double *) Calloc(*max_haps, double);
 
  if(prior==NULL){
    errmsg("could not alloc mem for prior");
  }

  /* array to keep track of loci used at any point in time */
  loci_used = (int *) Calloc(n_loci, int);
  if(loci_used==NULL){
    errmsg("could not alloc mem for loci_used");
  }

  /* array of pointers to haplo information */
  hap_list = (HAP **) Calloc(*max_haps, HAP* );
  if(hap_list==NULL){
    errmsg("could not alloc mem for hap_list");
  }


  /* put geno data into haplo list */
  
  pair_id = - 1;
  n_hap=0;

  for(i=0;i< *n_subject;i++){

    pair_id++;

    indx1 = n_hap;
    n_hap++;
    indx2 = n_hap;
    n_hap++;

    hap_list[indx1] = new_hap(i, pair_id, weight[i], 0.0, 1.0);
 
    hap_list[indx2]  = new_hap(i, pair_id, weight[i], 0.0, 1.0);

    k=0;
    for (j=0; j< n_loci; j++) {
	   (hap_list[indx1])->loci[j] = geno[i][k++];
	   (hap_list[indx2])->loci[j] = geno[i][k++];
    }

  }

  /* set seed for random unif generator, if needed */

  if(*random_start){
    ranAS183_seed(*iseed1, *iseed2, *iseed3);
  }



  /* begin haplotype algorithm */

  if(*verbose){

    REprintf("min_posterior = %8.5f\n",*min_posterior);
    REprintf("min_prior     = %8.5f\n",*min_prior);

    REprintf("loci_insert_order = ");
    for(i=0;i<n_loci;i++){
      REprintf("%i ",loci_insert_order[i]);
    }
    REprintf("\n\n");
  }


  is=0;
  ie= imin(*insert_batch_size, n_loci);
  n_batch=0;

  do {
    n_batch++;

    if(*verbose){
      REprintf("Inserting batch %i, loci= ",n_batch);
        for(i=is; i < ie ;i++){
          REprintf("%i ",loci_insert_order[i]);
         }
         REprintf("\n");
     }

     /* sort according to subj id, hap pair id, before insert & expand */
     qsort(hap_list, n_hap, sizeof(HAP *), cmp_subId_hapPairId);

     /* insert batch of loci */
     for(i=is; i < ie ;i++){
       insert_loc = loci_insert_order[i];
       n_hap = hap_enum(&hap_list, &prior, max_haps, n_alleles, insert_loc, n_hap, &pair_id);
     }


    /* sort according to subj id, hap pair id, after insert & expand */
    qsort(hap_list, n_hap, sizeof(HAP *), cmp_subId_hapPairId);

 
    /* set post for newly expanded haplos */
    set_posterior(n_hap, hap_list, random_start);

  
    if(*verbose){
      REprintf("\nhap_list after insert batch %i & set_post, before code haplo\n\n",n_batch);
      write_hap_list(hap_list, n_hap);
    }

    /* sort according to haplotype order - needed for computing unique haplos and their codes */
    qsort(hap_list, n_hap, sizeof(HAP *), cmp_hap);

 
    /* compute hap codes when computing n_u_hap */
    n_u_hap= code_haps(n_hap, hap_list);

  
    /* last sort before EM, according to subj id, then hap pair id */
     qsort(hap_list, n_hap, sizeof(HAP *), cmp_subId_hapPairId);

    if(*verbose){
      REprintf("\nhap_list: %4i after code haplo, before EM\n",n_batch);
      write_hap_list(hap_list, n_hap);
    }


    /* begin EM iterations */

    n_iter = 0;
    lnlike = 0.0;
    (*converge) = 0;

    for(iter = 0; iter< (*max_iter); iter++){

      n_iter++;

      hap_prior(n_hap, hap_list, prior, n_u_hap, *min_prior); 

      n_trim = hap_posterior(n_hap, hap_list, prior, n_u_hap, *min_posterior, &lnlike);

      if(*verbose){
        REprintf("\nprior probabilities\n\n");
        write_prior(n_u_hap, prior);
        REprintf("\nhap_list after compute posterior (n_trim = %d))\n\n",n_trim);
        write_hap_list(hap_list, n_hap);
        REprintf("     iter = %3i, max_iter=%3i, lnlike = %f\n",iter, *max_iter, lnlike);
      }

       /* check for convergence */
       if(iter==0) {
          lnlike_old = lnlike;
          continue;
       } 
        else {
          if (fabs(lnlike - lnlike_old) < *tol){
            (*converge) = 1;
             break;
          } 
          else {
	    lnlike_old = lnlike;
	  }
	}

     } /* end of EM loop */

    if( (*converge)==0){        
      /* Replaced with call to REprintf for 4.1.x  
	 PROBLEM "failed to converge for batch %i after %i iterations", n_batch, n_iter
	 RECOVER(NULL_ENTRY);
      */
      REprintf("failed to converge for batch %i after %i iterations", n_batch, n_iter);
    }


    divideKeep(hap_list, n_hap, &len_hap_list);
    n_hap = len_hap_list;


    if(*verbose){
      /*REprintf("\nhap_list after EM and after divideKeep \n\n",n_trim);*/
      write_hap_list(hap_list, n_hap);
    }
     
   
    /* update priors, in case haplos were trimmed during posteior calculations */
    
    hap_prior(n_hap, hap_list, prior, n_u_hap, *min_prior); 
    
    if(*verbose){
      if( (*converge)==1){
	REprintf("\n\nConverged after batch insertion, lnlike = %8.5f, n_iter = %i\n\n", lnlike, n_iter);
        }
      }

      is = ie;
      ie = is + imin(*insert_batch_size, (n_loci-is));

  } while(is < n_loci); /* end inserting all loci */


  /* copy values to return to S */
 
  *S_lnlike = lnlike;

  *n_hap_pairs = n_hap/2;

  /* Because some haplotypes may have been trimmed, we need to determine the number
     of unique haplotypes remaining after trimming */
 
  /* sort according to haplotype code - needed for computing unique haplos */
 
  qsort(hap_list, n_hap, sizeof(HAP *), cmp_hap_code);
 
  n_u_hap = count_unique_haps(n_hap, hap_list);
  *S_n_u_hap = n_u_hap;

  
 /* prepare to return info for unique haplotypes */
  u_hap_list = (HAPUNIQUE **) Calloc(n_u_hap, HAPUNIQUE *);
  if (!u_hap_list){
    errmsg("could not alloc mem for unique haplo");
  }

  unique_haps(n_hap, hap_list, u_hap_list, prior);

  if(*verbose){
    REprintf("\nn_u_hap = %d\n",n_u_hap);
    REprintf("\nunique haps\n\n"); 
    write_unique_hap_list(u_hap_list, n_u_hap); 
  }

  ret_u_hap_list = u_hap_list;

  /* prepare to return info for subjects */

  qsort(hap_list, n_hap, sizeof(HAP *), cmp_subId_hapPairId);
  ret_hap_list = hap_list;

  if(*verbose){
    REprintf("ret_hap_list\n");
    write_hap_list(ret_hap_list, n_hap);
  }


  /* the following ret (return) values are used for array sizes, for 
     copying data into S arrays, and for later freeing memory */

  ret_n_hap=n_hap;
  ret_n_u_hap = n_u_hap;
  ret_max_haps = (*max_haps);

  /* Free memory */

  Free(prior);
  prior = NULL;

  Free(loci_used);
  loci_used = NULL;

  for(i=0; i< (*n_subject); i++){
    Free(geno[i]);
  }
  Free(geno);
  geno = NULL;
 
}

/***********************************************************************************/

static HAP* new_hap(int id, int pair_id, double wt, double prior, double post){
  HAP *result;
  int *loc;

  result = (HAP *) Calloc(1, HAP);
 
 if (!result){
  errmsg("could not alloc mem for new hap");
  }

  result->id = id;
  result->pair_id = pair_id;
  result->wt = wt;
  result->post  = post;
  result->keep = 1;

  loc = (int *) Calloc(n_loci, int);
  if (!loc) {
    errmsg("could not alloc mem for new hap");
    Free(result);
  }

  result->loci = loc; 

  return result;
}

/***************************************************************************/

static void write_hap_list(HAP** so, int n_hap){
  int i,j;

  REprintf("subID     wt hapPairID hapCode keep");
  for(i=0;i<n_loci;i++){
     if(loci_used[i]==0) continue; 
    REprintf(" L%2d",i);
  }
  REprintf("    post\n");

  for(i=0; i< n_hap ;i++){
    REprintf("%5d %6.4f %9d %7d %4i", so[i]->id, so[i]->wt, so[i]->pair_id,so[i]->code,so[i]->keep);
    for(j=0;j<n_loci;j++){
       if(loci_used[j]==0) continue; 
      REprintf("%4d",so[i]->loci[j]);
    }

    REprintf("    %6.4f", so[i]->post);
    REprintf("\n");
  }
}

/***********************************************************************************/

static void write_unique_hap_list(HAPUNIQUE** so, int n_hap){
  int i,j;

  REprintf("hapCode keep");
  for(i=0;i<n_loci;i++){
     if(loci_used[i]==0) continue; 
    REprintf(" L%2d",i);
  }
  REprintf("  prior\n");

  for(i=0; i< n_hap ;i++){
    REprintf("%6d %4i",so[i]->code,so[i]->keep);
    for(j=0;j<n_loci;j++){
       if(loci_used[j]==0) continue; 
      REprintf("%4d",so[i]->loci[j]);
    }

    REprintf("    %6.4f", so[i]->prior);
    REprintf("\n");
  }
}

/****************************************************************************/

static void write_prior(int n, double *prior){
  int i;

  REprintf("hapCode  prior\n");
  for(i=0;i<n;i++){
    REprintf(" %5d  %6.4f\n", i, prior[i]);
  }

}

/****************************************************************************/

static int CDECL cmp_hap(const void *to_one, const void *to_two){
  int i;
  int *loc1, *loc2;
  int a1, a2;
  HAP *one, *two;
  one = * (HAP **) to_one;
  two = * (HAP **) to_two;
  loc1 = one->loci;
  loc2 = two->loci;
  for (i=0; i<n_loci; i++) {
    if(loci_used[i]==0) continue;
    a1 = loc1[i];
    a2 = loc2[i];
    if (a1<a2) return -1;
    if (a1>a2) return +1;
  }
  return 0;
}

/***********************************************************************************/

static int CDECL cmp_hap_code(const void *to_one, const void *to_two){
  HAP *one, *two;
  one = * (HAP **) to_one;
  two = * (HAP **) to_two;
  if((one->code)  <  (two->code)) return -1;
  if((one->code)  >  (two->code)) return  1;
  return 0;
}


/***********************************************************************************/

static int CDECL cmp_subId_hapPairId(const void *to_one, const void *to_two){
 
  /* Using this comparision function with qsort results in a sort first on subj id, 
    then on hap pair_id */

  HAP *one, *two;
  one = * (HAP **) to_one;
  two = * (HAP **) to_two;
 
  if((one->id)  < (two->id)) return -1;
  if((one->id)  > (two->id)) return  1;
  
 
  if( (one->pair_id) < (two->pair_id)) return -1;
  if( (one->pair_id) > (two->pair_id)) return 1;

  return 0;
}




/***********************************************************************************/

static void unique_haps(int n_hap, HAP **hap_list, HAPUNIQUE **u_hap_list,
                        double *prior) {

 /* assumes hap_list is sorted by either haplotype (cmp_hap)
     or haplotype code (cmp_trim) */

  HAP **hs, **he, **h;

  hs = hap_list;
  he = hap_list + n_hap;
 
  while (hs < he) {
    h = hs;
    do {
      h++;
    } while ( (h<he) &&  ((*hs)->code == (*h)->code) );
    *u_hap_list++ = copy_hap_unique(*hs, prior);
    hs = h;
  }

}

/***********************************************************************************/

static HAPUNIQUE* copy_hap_unique(HAP *old, double *prior) {
  HAPUNIQUE *result;
  int i;
  result = (HAPUNIQUE *) Calloc(1, HAPUNIQUE);
  if (result) {
    result->code    = old->code;
    result->prior   = prior[old->code];
    result->keep    = old->keep;
    result->loci = (int *) Calloc(n_loci, int);
    if (result->loci==NULL) {
      errmsg("could not alloc mem for copy_hap_unique");
      Free(result);
    }
    for (i=0; i<n_loci; i++) 
	result->loci[i] = old->loci[i];
  } 
  return result;
}


/***********************************************************************************/

static int code_haps(int n_hap, HAP **hap_list) {

  /* assumes hap_list is sorted by either haplotype (cmp_hap)
     or haplotype code (cmp_trim) */

  HAP **hs, **he, **h;
  int res = 0;
  hs = hap_list;
  he = hap_list + n_hap;
  while (hs < he) {
    h = hs;
    do {
      (*h)->code = res;
      h++;
    } while ((h<he) && (cmp_hap(hs, h)==0));
    res++;
    hs = h;
  }
  return res;
}
/***********************************************************************************/

static int count_unique_haps(int n_hap, HAP **hap_list) {

  /* assumes hap_list is sorted by either haplotype (cmp_hap)
     or haplotype code (cmp_hap_code) */

  HAP **hs, **he, **h;
  int res = 0;
  hs = hap_list;
  he = hap_list + n_hap;
  while (hs < he) {
    h = hs;
    do {
      h++;
    } while ( (h<he) && ( (*hs)->code == (*h)->code) );
    res++;
    hs = h;
  }
  return res;
}


/***********************************************************************************/

static int hap_enum(HAP ***hap_list_ptr, double **prior_ptr, int *max_haps, int *n_alleles, int insert_loc, 
                int n_hap, int *pair_id_ptr){

  int i,j, a_poss,a1_poss,a2_poss, a1, a2,a1_new,a2_new;
  int n_al, n_miss;
  HAP *h1, *h2, *h1_new, *h2_new;
 
  j = n_hap - 1;

  loci_used[insert_loc] = 1;
 
  for(i=0;i<(n_hap-1);i+=2){

    h1 = (*hap_list_ptr)[i];
    h2 = (*hap_list_ptr)[i+1];
    a1 = h1->loci[insert_loc];
    a2 = h2->loci[insert_loc];

    /* fill in missing allele values */

    n_al = n_alleles[insert_loc];

    n_miss = 0;
    if(a1==0) n_miss ++;
    if(a2==0) n_miss ++;
 
  switch(n_miss){
 
  case 0:
    if((a1!=a2) && (num_het(h1,h2) > 1) ){

      /* note that nhet = number of het loci that are currently in use,
         including new insert locus. Only need to consider reciprocal
         haplotype allele insertion if het at current insert locus, and
         total num of hets across all used loci > 1 */

      insert_new_hap_pair(hap_list_ptr, prior_ptr, max_haps, insert_loc,
                       h1, h2, a2, a1, pair_id_ptr, &j);

 
    }
    break;

  case 1:
       /* over-write haps for first possible alleles, to fill in one
	  possible haplotype pair, and expand if needed */

      if(a1==0){
        a1_new = 1;
        a2_new = a2;
       } else {
        a1_new = a1;
        a2_new = 1;
       }
      h1 ->loci[insert_loc] = a1_new;
      h2 ->loci[insert_loc] = a2_new;
      (*hap_list_ptr)[i]   = h1;
      (*hap_list_ptr)[i+1] = h2;

     if((a1_new!=a2_new) && (num_het(h1,h2) > 1) ){

        insert_new_hap_pair(hap_list_ptr, prior_ptr, max_haps, insert_loc,
                       h1, h2, a2_new, a1_new, pair_id_ptr, &j); 
   
     }
  
     /* now consider all other values of missing allele */

     for(a_poss=2;a_poss<=n_al;a_poss++){
       
        if(a1==0){
          a1_new = a_poss;
          a2_new = a2;
         } else {
          a1_new = a1;
          a2_new = a_poss;
         }

        insert_new_hap_pair(hap_list_ptr, prior_ptr, max_haps, insert_loc,
                       h1, h2, a1_new, a2_new, pair_id_ptr, &j); 
       
        /* pull out the newly inserted hap pair, to be used to
           determine number of heterozous sites, to determine
           whether new hap pair needs to be inserted */
 
         h1_new = (*hap_list_ptr)[j-1];
         h2_new = (*hap_list_ptr)[j];
 
        if((a1_new!=a2_new) && (num_het(h1_new,h2_new) > 1) ){
  
           insert_new_hap_pair(hap_list_ptr, prior_ptr, max_haps, insert_loc,
                       h1, h2, a2_new, a1_new, pair_id_ptr, &j); 
           
        }
     }
     break;
  
  case 2:
      /* over-write haps for first possible alleles, to fill in one
	  possible haplotype pair, and expand if needed */
    
     h1 ->loci[insert_loc] = 1;
     h2 ->loci[insert_loc] = 1;
     (*hap_list_ptr)[i]   = h1;
     (*hap_list_ptr)[i+1] = h2;

     for(a1_poss=1;a1_poss<=n_al;a1_poss++){
       for(a2_poss=a1_poss; a2_poss<=n_al;a2_poss++){

	 if( (a1_poss==1) && (a2_poss==1) ) continue; /* did this case above */
 
         a1_new = a1_poss;
         a2_new = a2_poss;
 
         insert_new_hap_pair(hap_list_ptr, prior_ptr, max_haps, insert_loc,
                       h1, h2, a1_new, a2_new, pair_id_ptr, &j); 
  
         h1_new = (*hap_list_ptr)[j-1];
         h2_new = (*hap_list_ptr)[j];

         if((a1_new!=a2_new) && (num_het(h1_new,h2_new) > 1) ){

             insert_new_hap_pair(hap_list_ptr, prior_ptr, max_haps, insert_loc,
                       h1, h2, a2_new, a1_new, pair_id_ptr, &j); 

	 }
       }
     }
     break;

   default:
    errmsg("error for number missing alleles");
  }
  }

  return (j + 1); /* return value is new number of haplos after all expanded */

}

/***********************************************************************************/

static HAP* copy_hap(HAP *old) {
  HAP *result;
  int i;
  result = (HAP *) Calloc(1, HAP);
  if (result) {
    result->id      = old->id;
    result->pair_id = old->pair_id;
    result->wt      = old->wt;
    result->post    = old->post;
    result->code    = old->code;
    result->keep    = old->keep;
    result->loci = (int *) Calloc(n_loci, int);
    if (result->loci==NULL) {
      errmsg("could not alloc mem for copy_hap");
      Free(result);
    }
    for (i=0; i<n_loci; i++) 
	result->loci[i] = old->loci[i];
  } 
  return result;
}


/***********************************************************************************/

static int num_het(HAP* h1, HAP* h2){
  int i, nhet;
  nhet = 0;
  for(i=0;i<n_loci;i++){
    if( (loci_used[i]==1) && (h1->loci[i]!=h2->loci[i]) )
      nhet++;
  }
  return nhet;
}

/***********************************************************************************/

static void hap_prior(int n_hap, HAP** hap_list, double *prior, int n_u_hap,
                      double min_prior) {

  double total, a;
  int i;

  for(i=0; i<n_u_hap; i++){
    prior[i] = 0.0;
  }


  total = 0.0;
  for(i =0; i<n_hap; i++){
    a = hap_list[i]->post * hap_list[i]->wt * hap_list[i]->keep;
    total += a;
    prior[hap_list[i]->code] += a;
  }

  for(i=0;i<n_u_hap;i++){
    prior[i] = prior[i]/total;

    if(prior[i] < min_prior){
      prior[i] = 0.0;
    }

  }

 
}

/***********************************************************************************/

static int hap_posterior(int n_hap, HAP **hap_list, double *prior, 
                         int n_u_hap, double min_posterior, double *lnlike) {


  HAP **hs, **he, **hn, **h, **h2;
  int id;
  double subtotal, gp, tmp_wt;
  int keep;
  int n_trim, total_trim;

  hs = hap_list;
  he = hap_list + n_hap;
  total_trim = 0;
  (*lnlike) = 0.0;
 
  while (hs < he) {

    h = hs;
    tmp_wt = (*h)->wt;
    subtotal = 0.0;
    n_trim = 0;
 
    /* numerator of post prob */
    do {
      id = (*h)->id;
      h2 = h+1;
      gp = prior[(*h)->code] * prior[(*h2)->code] ;
      if ((*h)->code != (*h2)->code)
	gp *= 2.0;
      subtotal += gp;
      (*h)->post = (*h2)->post = gp;
      h = h2+1;
    } while ((h<he) && (((*h)->id)==id));
 
    hn = h;
    
 
    if(subtotal > 0.0){

      /* check if need to trim by post */
      for (h=hs; h<hn; h+=2) {
       keep = ((*h)->post/subtotal  < min_posterior) ? 0 : 1;
       if(keep==0){ /* trim pair of haps */
          n_trim +=2;
          subtotal -= (*h)->post ;
          (*h)->post =  0.0;
          (*h)->keep = 0;
          (*(h+1))->post = 0.0;
          (*(h+1))->keep = 0;
       }
      }
       /* rescale if new subtotal > 0.0 */
        if(subtotal > 0.0){
          for (h=hs; h<hn; h++) {
	    (*h)->post = (*h)->post/subtotal;
	  }
	}
       /* zero post and trim all if new subtotal <= 0.0 */
       else {
        for (h=hs; h<hn; h++) {
	  (*h)->post =0.0;
          (*h)->keep = 0;
	}
       }
    }
    /* if original subtotal <= 0, zero post and trim all */
    else {
      for (h=hs; h<hn; h++) {
	  (*h)->post = 0.0;
          (*h)->keep = 0;
      }
    }

    (*lnlike) += (subtotal > 0.0) ? tmp_wt * log(subtotal) : 0.0;
    total_trim += n_trim;
    hs = hn;
  }

    return total_trim;
}

/*********************************************************************************/
static void set_posterior(int n_hap, HAP **hap_list, int *random_start){
  HAP **hs, **he, **hn, **h, **h1, **h2;
  double u, subtotal, post;
  int id;

  hs = hap_list;
  he = hap_list + n_hap;


  /* fill numertators of post */
  if(! (*random_start) )
  {
     while(hs < he){
       h1=hs;
       hs++;
       h2=hs;
       (*h1)->post = (*h2)->post = 1.0;
       hs++;
     }
  } 
  else {
     while(hs < he){
       u = ranAS183();
       h1=hs;
       hs++;
       h2=hs;
       (*h1)->post = (*h2)->post = u;
       hs++;
     }
  }


  /* standardize so post sums to 1 per subject */
 
    hs = hap_list;
    he = hap_list + n_hap;

    while(hs < he){

      subtotal = 0.0;
      h = hs;

      do {
        id = (*h)->id;
        subtotal += (*h)->post;
        h += 2;
      } while ( (h<he) && ( (*h)->id == id ) );

      hn = h; /* new end for a subject */

   
      for(h = hs; h < hn; h+=2){
        post = (*h)->post/subtotal;
        (*h)->post = post;
	(*(h+1))->post = post;
      }

      hs = hn; /* new begin for next subject */

    }


    return ;
}

/*********************************************************************************/

static int **int_matrix(int nrow, int ncol){
/* allocate int matrix with subscript range m[0 ..(nrow-1)][0..(ncol-1)] */
        int i;
        int **m;

        /* allocate pointers to rows */
        m=(int **) Calloc(nrow, int *);
        if (!m) errmsg("mem alloc failure 1 in int_matrix");
  
	/* allocate vec of memory for each row */
        for(i=0;i<nrow;i++) {
          m[i]=(int *) Calloc(ncol, int);
          if(!m[i]) errmsg("mem alloc failure 2 in int_matrix");
	}

        /* return pointer to array of pointers to rows */
        return m;
}

/***********************************************************************************/

static int **int_vec_to_mat(int *Yvec, int nrow, int ncol){

   int i,j,k;
   int **Y;

   Y=int_matrix(nrow,ncol);
   k=0;
   for (j=0;j<ncol;j++){
      for (i=0;i<nrow;i++){
         Y[i][j]=Yvec[k];
         k++;
      }
   }
   return Y;
}

/***********************************************************************************/

void haplo_em_ret_info(
   int   n_u_hap,      /* number of unique hapoltypes                           */
   int   S_n_loci,     /* number of loci                                        */
   int   n_pairs,      /* number of pairs of loci over all subjects             */
   double *hap_prob,     /* probabilities for unique haplotypes, length= n_u_hap  */
   int   *u_hap,        /* unique haplotype, length=n_u_hap * n_loci             */
   int   *u_hap_code,   /* code for unique haplotypes, length=n_u_hap            */
   int   *subj_id,      /* subject id = index of subject                         */
   double *post,         /* posterior probability of pair of haplotypes           */
   int   *hap1_code,    /* code for haplotype-1 of a pair, length=n_pairs        */
   int   *hap2_code     /* code for haplotype-2 of a pair, length=n_pairs        */
  )
{


  int i,j,k;
  HAP **h;
  k= -1;
  for(i=0;i<n_u_hap;i++){
    hap_prob[i] = ret_u_hap_list[i]->prior;
    u_hap_code[i] = ret_u_hap_list[i]->code;
    for(j=0;j<S_n_loci;j++){
      k++;
      u_hap[k] = ret_u_hap_list[i]->loci[j];
    }
  }

  h = ret_hap_list;
  for(i=0; i<n_pairs; i++){
    subj_id[i] = (*h)->id;
    post[i] = (*h)->post;
    hap1_code[i] = (*h)->code;
    h++;
    hap2_code[i] = (*h)->code;
    h++;
  }


  return;
}

/***********************************************************************************/

void haplo_free_memory(void){

  /* free memory saved for returned info */

  int i;


  for(i=0;i<ret_max_haps;i++){
    if(ret_hap_list[i] != NULL) {
      if(ret_hap_list[i]->loci != NULL) Free( ret_hap_list[i]->loci );
      Free( ret_hap_list[i]); 
    }
  }


  Free(ret_hap_list);

  ret_hap_list = NULL;

  for(i=0;i<ret_n_u_hap;i++){
    if(ret_u_hap_list[i] != NULL){
      if(ret_u_hap_list[i]->loci != NULL) Free( ret_u_hap_list[i]->loci );
       Free( ret_u_hap_list[i] );
    }
  }

  Free(ret_u_hap_list);

  ret_u_hap_list = NULL;

  return;
}

/***********************************************************************************/

/*
     Algorithm AS 183 Appl. Statist. (1982) vol.31, no.2

     Returns a pseudo-random number rectangularly distributed
     between 0 and 1.   The cycle length is 6.95E+12 (See page 123
     of Applied Statistics (1984) vol.33), not as claimed in the
     original article.

     ix, iy and iz should be set to integer values between 1 and
     30000 before the first entry. To do this, 
     first call ranAS183_seed(iseed1,iseed2,iseed3), where iseed#
     are 3 int seeds between 1 and 30000. The 3  seeds are
     saved, but ix,iy,iz can change.

     NOTE: Feb 23, 2007 DJS changed long to int

    Translated from fortran to C.
*/

static int ix, iy, iz;

static int ranAS183_seed(int iseed1, int iseed2, int iseed3)
{
  int error;

  error=1;
  if( ( (iseed1 >=1) && (iseed1 <=30000)) && ( (iseed2 >=1) && (iseed2 <=30000) ) && 
      ( (iseed3 >=1) && (iseed3 <=30000) )) error=0;
  if(error) return (error);
  ix = iseed1;
  iy = iseed2;
  iz = iseed3;
  return (error);
}

/***********************************************************************************/

static double ranAS183(void)
{
   double u;

   ix = (171*ix) % 30269;
   iy = (172*iy) % 30307;
   iz = (170*iz) % 30323;
   u  = (double)ix/30269.0 + (double)iy/30307.0 + (double)iz/30323.0;
   return ( u - (int) u );
}

/***********************************************************************************/
static void errmsg(char *string){

  /* Function to emulate "stop" of S+ - see page 134, S Programing, by
     Venables and Ripley */

  /* PROBLEM "%s", string RECOVER(NULL_ENTRY);
     Replace with call to Rf_error for R 4.1.x 
  */
  //Rf_error(string, "%s");
  REprintf("%s", string);
}


/***********************************************************************************/

static void divideKeep(HAP **hap_list, int n, int *nReturn)
{
  int i,j;
  HAP *temp;
  int nValid = 0;


 i = -1;
  for(j = i+1; j<n; j++){
    if(hap_list[j]->keep !=0){
        i++;
        temp = hap_list[i];
        hap_list[i] = hap_list[j];
	hap_list[j] = temp;
  }
  }

 
  for(i = 0; i<n; i++){
    if( hap_list[i]->keep == 0) continue;
     nValid++;
  }


  *nReturn = nValid;


  return;
}

/***********************************************************************************/

static void add_more_memory(HAP ***hap_list, double **prior,int *max_haps){


  /* check that max_haps will not exceed max limit for an int on a 32-bit processor */
  

  if(*max_haps ==  INT_MAX)
    {
      errmsg("cannot increase max_haps, already at max limit");
    }

  if((*max_haps) > INT_MAX/2)
    {
      *max_haps = INT_MAX;
    } 
  else 
    {
      *max_haps = 2 * (*max_haps);
    }


  double *new_prior =  (double *) Realloc(*prior, *max_haps, double);
  if(new_prior==NULL){
    errmsg("could not realloc mem for prior");
  }
  *prior = new_prior;
  
  HAP **new_hap_list = (HAP **) Realloc(*hap_list, *max_haps, HAP* );
  if(new_hap_list==NULL){
    errmsg("could not realloc mem for hap_list");
  }
  *hap_list = new_hap_list;
  
  return;
}

/***********************************************************************************/

static void insert_new_hap_pair(HAP ***hap_list_ptr, double **prior_ptr, 
                                int *max_haps, int insert_loc,
                                HAP *h1_old, HAP *h2_old, 
                                int a1_new, int a2_new,
                                int *pair_id_ptr, int *j){  

  loci_used[insert_loc] = 1;


  if(  ((*j)+2)  >= (*max_haps) ){
     add_more_memory(hap_list_ptr, prior_ptr, max_haps);
  }

  /* update pair id, to be used for both haplotypes */

 (*pair_id_ptr) ++;
 
  /* By using divideKeep, the number of haploytpes (nhap) is reduced to only
     those with keep=1, but the memory for those with keep=0 is still in place.
     So, when adding new haplotypes to the 'end' of the list, nhap gives a count
     that is shorter than the true length. If where we are adding a haplotype in a list is
     not NULL, then simply over write existing memory with old haplotype data, and then
     update this old info with new alleles at insterted locus position, as well a pair_id.
     If where we are adding points to NULL, then need to copy old haplotype info (while
     allocating memory), then update inserted allele and pair_id.
  */


  /* First haplotype */
  (*j)++;

  if( (*hap_list_ptr)[*j] !=NULL)
   {
     overwrite_hap((*hap_list_ptr)[*j], h1_old);
    }
   else 
    {
     (*hap_list_ptr)[*j]  = copy_hap(h1_old);
    }

   (*hap_list_ptr)[*j]->loci[insert_loc] = a1_new;
   (*hap_list_ptr)[*j]->pair_id = (*pair_id_ptr);
 

   /* Second haplotype */

   (*j)++;

   if( (*hap_list_ptr)[*j] !=NULL)
   {
      overwrite_hap((*hap_list_ptr)[*j], h2_old);
    }
   else 
    {
     (*hap_list_ptr)[*j]  = copy_hap(h2_old);
    }

   (*hap_list_ptr)[*j]->loci[insert_loc] = a2_new;
   (*hap_list_ptr)[*j]->pair_id = (*pair_id_ptr);
 


}

/***********************************************************************************/

static void overwrite_hap(HAP *new, HAP *old) {

    int i;

    new->id      = old->id;
    new->pair_id = old->pair_id;
    new->wt      = old->wt;
    new->post    = old->post;
    new->code    = old->code;
    new->keep    = old->keep;
 

    if(new->loci == NULL){
       new->loci = (int *) Calloc(n_loci, int);
    }
    if(new->loci == NULL) {
      errmsg("could not alloc mem for overwrite_hap");
    }

    for (i=0; i<n_loci; i++){
	new->loci[i] = old->loci[i];
    }
}

/***********************************************************************************/

void checkIntMax(int *intMax) {

  *intMax = INT_MAX;

  return ;
}

int haplo_em_pin_wrap(int n_loci, 
	      int n_subject,
	      double weight[],
	      int n_alleles[], 
	      int max_haps,
	      int max_iter,
	      int loci_insert_order[],
	      double min_prior,         /* trim haplo's with prior < min_prior            */
	      double min_posterior,
	      double tol,
	      int insert_batch_size,
	      int random_start,
	      int iseed1,
	      int iseed2,
	      int iseed3,
	      int verbose,
	      int geno_vec[],

	      /* the following are returned values */	      
	      int *converge,             /* convergence indicator for EM                   */
	      double *S_lnlike,          /* lnlike from final EM                           */
	      int *S_n_u_hap,            /* number of unique haplotypes                    */
	      int *n_hap_pairs           /* total number of pairs of haplotypes over all   */
)

{
  haplo_em_pin(
	 &n_loci,              
         &n_subject,          
         weight,            
         geno_vec,          
         n_alleles,         
         &max_haps,          
         &max_iter,          
         loci_insert_order, 
         &min_prior,         
         &min_posterior,     
         &tol,               
         &insert_batch_size, 
         converge,          
         S_lnlike,          
         S_n_u_hap,         
         n_hap_pairs,       
         &random_start,      
         &iseed1,            
         &iseed2,
         &iseed3,
         &verbose
	 );   
  return 0;
}

int haplo_em_ret_info_wrap(
       double S_n_u_hap,   // number of unique hapoltypes                           
       int n_loci,         // number of loci                                        
       int n_hap_pairs,    // number of pairs of loci over all subjects             

       /* all the following arguments are returned arrays */
       /* each array is prepended by the length of the array passed in from Python */
       /* all memory allocation is done in Python typemaps before body of function */
       int hap_prob_len,   double *hap_prob, // probabilities for unique haplotypes, length= n_u_hap  
       int u_hap_len,      int *u_hap,       // unique haplotype, length=n_u_hap * n_loci             
       int u_hap_code_len, int *u_hap_code,  // code for unique haplotypes, length=n_u_hap            
       int subj_id_len,    int *subj_id,     // subject id = index of subject                         
       int post_len,       double *post,     // posterior probability of pair of haplotypes           
       int hap1_code_len,  int *hap1_code,   // code for haplotype-1 of a pair, length=n_pairs        
       int hap2_code_len,  int *hap2_code    // code for haplotype-2 of a pair, length=n_pairs
			   )
{
  haplo_em_ret_info(
       S_n_u_hap,   
       n_loci,     
       n_hap_pairs, 
       hap_prob,   
       u_hap, 
       u_hap_code, 
       subj_id,    
       post,    
       hap1_code, 
       hap2_code  
     );

#if DEBUG
  {
    int i, j, k;
    printf("START inside C program\n");
    printf("n_loci: %d\n", n_loci);
    k = -1;
    printf("i hap_prob[i]   u_hap_code[i]   k   u_hap[k]\n");
    for(i=0;i < S_n_u_hap;i++){
      printf("%2i  %8.5f       %3d       ", i, hap_prob[i], u_hap_code[i]);
      printf(" %3d ", k+1 );
      for(j=0;j<n_loci;j++){
	k++;
	printf(" %3d ", u_hap[k]);
      }
      printf("\n");
    }
    printf("hap1   hap2\n");
    for(i=0;i < n_hap_pairs;i++) {
      printf("%3d  %3d\n", hap1_code[i], hap2_code[i]);
    }

    printf("END inside C program\n");
  }
#endif

  return 0;
}

/* a main function that calls haplo_em_pin() */
int main( void ) {
     int index;

     /* example from haplo.stats: hla.demo[,c(17,18,21:24)]; label <-c("DQB","DRB","B") */
     int n_loci = 2;
     int n_subject = 5;
     double weight[ ] = { 1, 1, 1, 1, 1 }; 
     int n_alleles[ ] = { 7, 7 };
     int max_haps = 18;
     int max_iter = 5000;
     int loci_insert_order[ ] = { 0, 1 };
     double min_posterior = 0.000000001;
     double tol = 0.00001;
     int insert_batch_size = 2;
     int random_start = 0;
     int iseed1 = 18717.63;
     int iseed2 = 16090.08;
     int iseed3 = 14502.41;
     int verbose = 0;
     int geno_vec[ ] = { 3, 2, 1, 4, 5, 6, 4, 7, 4, 6, 7, 1, 2, 1, 4, 6, 3, 7, 3, 5 };
     //     int geno_vec[ ] = { 4, 2, 1, 7, 8,11, 7,13, 7,11,62, 7,27, 7,51,61,44,62,44,55 };

     // data structures that are returned
     double *hap_prob;    /* probabilities for unique haplotypes, length= n_u_hap  */
     int   *u_hap;        /* unique haplotype, length=n_u_hap * n_loci             */
     int   *u_hap_code;   /* code for unique haplotypes, length=n_u_hap            */
     int   *subj_id;     /* subject id = index of subject                         */
     double *post;         /* posterior probability of pair of haplotypes           */
     int   *hap1_code;    /* code for haplotype-1 of a pair, length=n_pairs        */
     int   *hap2_code;     /* code for haplotype-2 of a pair, length=n_pairs        */

/* Larger example with n=50 & 3 loci
     int n_loci = 3;
     int n_subject = 50;
     double weight[ ] = { 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 };
     int n_alleles[ ] = { 7, 7 };
     int max_haps = 320;
     int max_iter = 5000;
     int loci_insert_order[ ] = { 0, 1, 2 };
     double min_posterior = 0.000000001;
     double tol = 0.00001;
     int insert_batch_size = 3;
     int random_start = 0;
     int iseed1 = 18717.63;
     int iseed2 = 16090.08;
     int iseed3 = 14502.41;
     int verbose = 0;
     int geno_vec[ ] = { 2,1,2,1,2,1,10,9,10,6,2,10,11,10,6,6,2,10,10,2,2,1,6,5,12,6,11,12,2,2,2,11,6,1,2,11,6,11,2,11,10,1,1,3,2,1,1,6,10,8,3,10,11,2,5,1,12,2,11,6,3,3,11,3,11,10,11,2,5,12,7,1,1,5,3,12,2,10,1,10,4,3,10,10,2,3,10,2,2,1,10,4,1,10,3,10,1,1,1,2,4,2,1,5,6,3,2,9,2,1,4,2,9,2,1,1,5,2,2,4,2,3,1,4,2,1,8,2,3,2,5,4,1,3,8,4,2,4,4,3,2,5,3,2,4,2,3,1,2,4,8,5,9,5,8,5,9,8,2,1,4,4,9,4,9,9,9,10,6,9,4,3,3,6,4,9,9,9,8,8,10,9,2,6,8,9,7,9,4,9,2,5,3,4,6,5,3,3,3,10,18,1,5,1,12,2,1,9,1,5,9,13,9,1,12,12,13,1,1,16,9,2,2,6,12,1,18,14,2,1,1,8,4,2,6,16,1,9,9,9,1,3,2,9,18,9,2,2,2,9,17,9,18,9,13,9,19,9,6,6,16,5,18,16,1,6,17,19,4,17,5,9,16,16,1,6,7,6,5,11,15,16,6,6,7,13,7,9,9,20,9,14,2,10,16,4,2,15,4,13 };
*/

     /* guessing at how to initialize these */
     double  min_prior = 0.0;          /* trim haplo's with prior < min_prior            */
     int     converge = 0;             /* convergence indicator for EM                   */
     double  S_lnlike = -9.9;          /* lnlike from final EM                           */
     int     S_n_u_hap = 3;            /* number of unique haplotypes                    */
     int     n_hap_pairs = 1;          /* total number of pairs of haplotypes over all   */
     int     prod1 = 1;
     int i, j, k;

     /* print geno_vec */
     printf("geno_vec = [");
     for(index = 0; index < 20; index++)
       printf( "%d, ", geno_vec[index]);
     printf("]\n");

     haplo_em_pin(
		  &n_loci,              
		  &n_subject,          
		  weight,            
		  geno_vec,          
		  n_alleles,         
		  &max_haps,          
		  &max_iter,          
		  loci_insert_order, 
		  &min_prior,         
		  &min_posterior,     
		  &tol,               
		  &insert_batch_size, 
		  &converge,          
		  &S_lnlike,          
		  &S_n_u_hap,         
		  &n_hap_pairs,       
		  &random_start,      
		  &iseed1,            
		  &iseed2,
		  &iseed3,
		  &verbose
		  );         

    printf("...TEST0.1 (S_lnlike , converge): %14.5f %i\n", S_lnlike , converge); //RS added
    prod1 = S_n_u_hap * n_loci;
    printf("...TEST0.2 (S_n_u_hap , n_loci, prod1): %i %i %i\n", S_n_u_hap , n_loci, prod1); //RS added

    hap_prob = (double *) Calloc(S_n_u_hap, double);
    u_hap = (int *) Calloc(S_n_u_hap * n_loci, int);
    u_hap_code = (int *) Calloc(S_n_u_hap, int);
    subj_id = (int *) Calloc(n_hap_pairs, int);
    post = (double *) Calloc(n_hap_pairs, double);
    hap1_code = (int *) Calloc(n_hap_pairs, int);
    hap2_code = (int *) Calloc(n_hap_pairs, int);
   
    haplo_em_ret_info(
       S_n_u_hap,   // number of unique hapoltypes                           
       n_loci,     // number of loci                                        
       n_hap_pairs, // number of pairs of loci over all subjects             
       hap_prob,   // probabilities for unique haplotypes, length= n_u_hap  
       u_hap, // unique haplotype, length=n_u_hap * n_loci             
       u_hap_code,   // code for unique haplotypes, length=n_u_hap            
       subj_id,    // subject id = index of subject                         
       post,    // posterior probability of pair of haplotypes           
       hap1_code,    // code for haplotype-1 of a pair, length=n_pairs        
       hap2_code     // code for haplotype-2 of a pair, length=n_pairs        
     );

    printf("inside main():\n");
    printf("n_loci: %d\n", n_loci);
    k = -1;
    printf("i hap_prob[i]   u_hap_code[i]   k   u_hap[k]\n");
    for(i=0;i<S_n_u_hap;i++){
      printf("%i  %8.5f  %d ", i, hap_prob[i], u_hap_code[i]);
      printf(" %d ", k+1 );
      for(j=0;j<n_loci;j++){
	k++;
	printf(" %d ", u_hap[k]);
      }
      printf("\n");
    }

    Free(hap_prob);
    Free(u_hap);
    Free(u_hap_code);
    Free(subj_id);
    Free(post);
    Free(hap1_code);
    Free(hap2_code);
    haplo_free_memory();

    return 0;
  } /* end main */
