/* SWIG interface generation file */

%module EWSlatkinExact

%include "typemap.i"
%{
extern int main_proc(int r_obs[], int k, int n, int maxrep);
extern double get_theta();
extern double get_prob_ewens();
extern double get_prob_homozygosity();
extern double get_mean_homozygosity();
extern double get_var_homozygosity();
%}

extern int main_proc(int r_obs[], int k, int n, int maxrep);
extern double get_theta();
extern double get_prob_ewens();
extern double get_prob_homozygosity();
extern double get_mean_homozygosity();
extern double get_var_homozygosity();

/*
 * Local variables:
 * mode: c
 * End:
 */
