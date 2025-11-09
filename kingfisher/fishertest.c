/* Just for testing, not part of Kingfisher program. */
/* Calculate Fisher's p for one rule X->A, given data size n, frx=fr(X),
   frxa=fr(XA), fra=fr(A) (absolute frequencies) */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "measures.h"
#include "glob.h"
#include <values.h>

int main(){
  int frxa=80;
  int frx=100;
  int fra=100;
  float lnp;
  long double neper=expl(1.0);
  n=1000; /* set n here, global variable */
  
  initlnfact(n); /* important: initialize ln-factorials first! */
  lnp=exactlnp(frxa,frx,fra,n);
  printf("lnp=%f p=%e\n",lnp,pow(neper,lnp));



  return EXIT_SUCCESS;
}
