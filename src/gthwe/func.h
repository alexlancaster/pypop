/* This file is part of PyPop
  
  Copyright (C) 1992. Sun-Wei Guo.
  Modifications Copyright (C) 1999, 2003, 2004. 
  The Regents of the University of California (Regents) All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS. */

/***************************************************************************
  func.h 

  header file containing the function names.

  status: modified from g-t program

  date: 12/15/99

***************************************************************************/

#include  <stdio.h>

char *ctime();
long int longmult(long p, long q);
long int linearrandomint(void);
void randominit(long int startingseed);
unsigned int fiborandomint(void);
long int randomrange(long r);

double log_factorial();
double ln_p_value();
double cal_prob();
double cal_const();

int check_file();
int read_data();
long init_rand();
int run_data();
void print_data();
void get_interval();
void select_index();
void cal_n();
void stamp_time();

double diff_statistic(int i, int j, int total_gametes, 
		      int *allele_array, int *genotypes);

double chen_statistic (int i, int j, int total_gametes, 
		       int *allele_array, int *genotypes);

void init_stats(char *statistic_type, 
		double (*statistic_func) (int, int, int, int *, int *),
		double *obs_normdev, int no_allele, int total_individuals,
		int *allele_array, int *genotypes,  FILE *outfile);

void store_stats(char *statistic_type, double (*statistic_func) 
		 (int, int, int, int *, int *),
		 double *obs_normdev, int *normdev_count, 
		 int no_allele, int total_individuals,
		 int *allele_array, int *genotypes, FILE *outfile);

void print_stats(char *statistic_type, int *normdev_count, 
		 int no_allele, double steps, FILE *outfile);
