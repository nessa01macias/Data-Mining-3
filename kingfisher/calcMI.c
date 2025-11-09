#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <values.h>
#include "measures.h"
#include "glob.h"


int main(){
  int fra=400;
  int frx=251;
  int frxa=203;
  double mi;  
  double elnp, pval;
  double neper=expl(1.0);
  float cval;
  
  n=500;
  initlnfact(n);
  mi=MI(frxa,frx,fra,n);
  elnp=exactlnp(frxa,frx,fra,n);
  pval=pow(neper,elnp);
  cval=chi2val(frxa,frx,fra,n);
  printf("MI=%.2e 2nMI=%.1e, p_F=%.2e, chi2=%.2f cf=%.3f\n",mi,2*n*mi,pval,cval,((float)frxa)/frx);

  

   return EXIT_SUCCESS;
}
