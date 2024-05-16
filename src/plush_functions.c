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

void print_boolean(int x){
    if(x){
        printf("true\n");
    }else{
        printf("false\n");
    }
}

void print_int_array(int* arr, int size){
    for(int i = 0; i < size; i++){
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void print_float_array(float* arr, int size){
    for(int i = 0; i < size; i++){
        printf("%f ", arr[i]);
    }
    printf("\n");
}

void print_string_array(char** arr, int size){
    for(int i = 0; i < size; i++){
        printf("%s ", arr[i]);
    }
    printf("\n");
}

void print_char_array(char* arr, int size){
    for(int i = 0; i < size; i++){
        printf("%c ", arr[i]);
    }
    printf("\n");
}

void print_boolean_array(int* arr, int size){
    for(int i = 0; i < size; i++){
        if(arr[i]){
            printf("true ");
        }else{
            printf("false ");
        }
    }
    printf("\n");
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

float* get_float_array(int size){
    return malloc(size * sizeof(float));
}

char* get_char_array(int size){
    return malloc(size * sizeof(char));
}

int* get_boolean_array(int size){
    return malloc(size * sizeof(int));
}




int** get_int_matrix(int row, int col){
    int** matrix = (int**)malloc(row * sizeof(int*));
    for(int i = 0; i < row; i++){
        matrix[i] = (int*)malloc(col * sizeof(int));
    }
    return matrix;
}

float** get_float_matrix(int row, int col){
    float** matrix = (float**)malloc(row * sizeof(float*));
    for(int i = 0; i < row; i++){
        matrix[i] = (float*)malloc(col * sizeof(float));
    }
    return matrix;
}

char*** get_string_matrix(int row, int col){
    char** matrix = (char**)malloc(row * sizeof(char*));
    for(int i = 0; i < row; i++){
        matrix[i] = (char*)malloc(col * sizeof(char));
    }
    return matrix;
}

char** get_char_matrix(int row, int col){
    char** matrix = (char**)malloc(row * sizeof(char*));
    for(int i = 0; i < row; i++){
        matrix[i] = (char*)malloc(col * sizeof(char));
    }
    return matrix;
}

int** get_boolean_matrix(int row, int col){
    int** matrix = (int**)malloc(row * sizeof(int*));
    for(int i = 0; i < row; i++){
        matrix[i] = (int*)malloc(col * sizeof(int));
    }
    return matrix;
}




