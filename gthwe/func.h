/***************************************************************************
  func.h 

  header file containing the function names.

  status: modified from g-t program

  date: 12/15/99

***************************************************************************/

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

