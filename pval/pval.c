#include "Rmath.h"

int main(int argc, char **argv) {

  /* printf("%s, %s\n", argv[1], argv[2]); */

  printf("pval: %f\n", 1-pchisq(0.1, 2.0, TRUE, FALSE));

}
