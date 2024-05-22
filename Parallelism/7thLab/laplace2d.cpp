#include <math.h>
#include <stdlib.h>
#include <cstring>
#include "laplace2d.hpp"
#include <stdio.h>

#include <cublas_v2.h>
#include <cuda_runtime.h>

#define OFFSET(x, y, m) (((x)*(m)) + (y))

void initialize(double *restrict A, double *restrict Anew, int m, int n){
    std::memset(A, 0, n * m * sizeof(double));
    std::memset(Anew, 0, n * m * sizeof(double));

    for(int i = 0; i < m; i++){
        A[i] = 10.0 + (20.0 - 10.0)/(m-1)*i;
        Anew[i] = 10.0 + (20.0 - 10.0)/(m-1)*i;

        A[n*(m-1) + i] = 20.0 + (30.0 - 20.0)/(m-1)*i;
        Anew[n*(m-1) + i] = 20.0 + (30.0 - 20.0)/(m-1)*i;
    }

    for(int i = 0; i < n; i++){
        A[m*i] = 10.0 + (20.0 - 10.0)/(n-1)*i;
        Anew[m*i] = 10.0 + (20.0 - 10.0)/(n-1)*i;

        A[m*i + n - 1] = 20.0 + (30.0 - 20.0)/(n-1)*i;
        Anew[m*i + n - 1] = 20.0 + (30.0 - 20.0)/(n-1)*i;
    }

    #pragma acc enter data copyin(A[:m*n],Anew[:m*n])
}

double calcNext(double *restrict A, double *restrict Anew, int m, int n, cublasHandle_t handle){

    double error = 0.0;
    const double alpha = 1.0 / 5.0;
    const double beta = 0.0;

    #pragma acc parallel loop reduction(max:error) present(A,Anew) vector_length(128) async
    for( int j = 1; j < n-1; j++){
        #pragma acc loop
        for( int i = 1; i < m-1; i++ ){
            Anew[OFFSET(j, i, m)] = ( A[OFFSET(j, i, m)] + A[OFFSET(j, i+1, m)] + A[OFFSET(j, i-1, m)] + A[OFFSET(j-1, i, m)] + A[OFFSET(j+1, i, m)]) / 5;
            error = fmax( error, fabs(Anew[OFFSET(j, i, m)] - A[OFFSET(j, i , m)]));
        }

        #pragma acc loop
        for( int i = 1; i < m-1; i++ ) A[OFFSET(j, i, m)] = Anew[OFFSET(j, i, m)];
    }
    #pragma acc wait

    return error;
}

void swap(double *restrict A, double *restrict Anew, int m, int n){
    #pragma acc parallel loop present(A,Anew) gang vector_length(128) async
    for( int j = 1; j < n-1; j++){
        #pragma acc loop vector
        for( int i = 1; i < m-1; i++ ) A[OFFSET(j, i, m)] = Anew[OFFSET(j, i, m)];
    }
    #pragma acc wait
}

void print_arr(double *restrict A, double *restrict Anew, int m, int n){
    #pragma acc parallel loop present(A,Anew) seq
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                printf("%6.2f ", A[i*m + j]);
            }
            printf("\n");
        }
}

void deallocate(double *restrict A, double *restrict Anew){
    #pragma acc exit data delete(A,Anew)
    free(A);
    free(Anew);
}
