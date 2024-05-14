#include <stdio.h>
#include <math.h>
#include <stdlib.h>

void print_int(int x){
    printf("%d\n", x);
}

void print_float(float x){
    printf("%f\n", x);
}

void print_string(char* s){
    printf("%s\n", s);
}

int power_int(int base, int e){
    return pow(base,e);
}

int* get_int_array(int size){
    return malloc(size * sizeof(int));
   
}

