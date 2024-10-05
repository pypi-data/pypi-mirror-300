/*
 * Generate testing csv files
 *
 *  cl xoshiro512-test-data-gen.c xoshiro512.orig.c /Ox
 * xoshiro512-test-data-gen.exe *
 *
 *  gcc xoshiro512-test-data-gen.c xoshiro512.orig.c /
 *  -o xoshiro512-test-data-gen
 *  ./xoshiro512-test-data-gen
 *
 */

#include "xoshiro512.orig.h"
#include <inttypes.h>
#include <stdio.h>

#define N 1000

int main() {
  uint64_t sum = 0;
  uint64_t state, seed = 0xDEADBEAF;
  state = seed;
  int i;
  /* SeedSequence(0xDEADBEAF).generate_state(8, dtype=np.uint64) */
  s[0] = 5778446405158232650;
  s[1] = 4639759349701729399;
  s[2] = 13222832537653397986;
  s[3] = 2330059127936092250;
  s[4] = 6380887635277085283;
  s[5] = 2943025801430425506;
  s[6] = 16158800551411432655;
  s[7] = 4467384082323269519;
  uint64_t store[N];
  for (i = 0; i < N; i++) {
    store[i] = next();
  }

  FILE *fp;
  fp = fopen("xoshiro512-testset-1.csv", "w");
  if (fp == NULL) {
    printf("Couldn't open file\n");
    return -1;
  }
  fprintf(fp, "seed, 0x%" PRIx64 "\n", seed);
  for (i = 0; i < N; i++) {
    fprintf(fp, "%d, 0x%" PRIx64 "\n", i, store[i]);
    if (i == 999) {
      printf("%d, 0x%" PRIx64 "\n", i, store[i]);
    }
  }
  fclose(fp);

  seed = state = 0;
  /* SeedSequence(0).generate_state(8, dtype=np.uint64) */
  s[0] = 15793235383387715774;
  s[1] = 12390638538380655177;
  s[2] = 2361836109651742017;
  s[3] = 3188717715514472916;
  s[4] = 648184599915300350;
  s[5] = 6643206648905449565;
  s[6] = 2726452650616012281;
  s[7] = 7074207863174652740;
  for (i = 0; i < N; i++) {
    store[i] = next();
  }
  fp = fopen("xoshiro512-testset-2.csv", "w");
  if (fp == NULL) {
    printf("Couldn't open file\n");
    return -1;
  }
  fprintf(fp, "seed, 0x%" PRIx64 "\n", seed);
  for (i = 0; i < N; i++) {
    fprintf(fp, "%d, 0x%" PRIx64 "\n", i, store[i]);
    if (i == 999) {
      printf("%d, 0x%" PRIx64 "\n", i, store[i]);
    }
  }
  fclose(fp);
}
