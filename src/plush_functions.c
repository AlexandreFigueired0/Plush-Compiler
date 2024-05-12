#include <stdio.h>
#include <math.h>
#include <stdlib.h>

void print_int(int x){
    printf("%d\n", x);
}

int power_int(int base, int e){
    return pow(base,e);
}

int* get_int_array(int size){
    return malloc(size * sizeof(int));
   
}

