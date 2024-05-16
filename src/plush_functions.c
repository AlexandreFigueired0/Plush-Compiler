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

void print_char(char c){
    printf("%c\n", c);
}

void print_int_array(int* arr, int size){
    for(int i = 0; i < size; i++){
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void print_boolean(int x){
    if(x){
        printf("true\n");
    }else{
        printf("false\n");
    }
}

int power_int(int base, int e){
    return pow(base,e);
}

int* get_int_array(int size){
    return malloc(size * sizeof(int));
}

char** get_string_array(int size){
    return malloc(size * sizeof(char*));
}


int** get_int_matrix(int row, int col){
    int** matrix = (int**)malloc(row * sizeof(int*));
    for(int i = 0; i < row; i++){
        matrix[i] = (int*)malloc(col * sizeof(int));
    }
    return matrix;
}


