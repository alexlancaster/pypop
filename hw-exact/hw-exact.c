int main(int argc, char *argv[])
{
  int numAlleles;
  int genotypes;
  int i;
  int *countTable = (int *)calloc(genotypes, sizeof(int));

  numAlleles = atoi(argv[1]);
  
  genotypes = numAlleles * (numAlleles + 1) / 2;

  for (i = 0; i < genotypes; i++) {
    countTable[i] = 3;
  }

  for (i = 0; i < genotypes; i++) {
    printf("%d = %d\n", i, countTable[i]);
  }

  free(countTable);
}


