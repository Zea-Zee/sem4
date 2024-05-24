#include <iostream>
#include <fstream>
#include <chrono>
#include <cmath>
#include <cstring>
#include <boost/program_options.hpp>
#include <cublas_v2.h>
#include <nvtx3/nvToolsExt.h>

using namespace std;
namespace po = boost::program_options;

void initialize(double *restrict A, double *restrict Anew, int m, int n);
double calcNext(double *restrict A, double *restrict Anew, int m, int n);
void swap(double *restrict A, double *restrict Anew, int m, int n);
void print_arr(double *restrict A, double *restrict Anew, int m, int n);
void deallocate(double *restrict A, double *restrict Anew);

int main(int argc, char** argv){
    unsigned int n, m, iter_max;
    double tol;
    bool showFlag;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "produce help message")
        ("NX", po::value<unsigned int>(&n)->default_value(128), "set NX")
        ("NY", po::value<unsigned int>(&m)->default_value(128), "set NY")
        ("TOLERANCE", po::value<double>(&tol)->default_value(1e-6), "set EPS")
        ("ITER", po::value<unsigned int>(&iter_max)->default_value(std::numeric_limits<unsigned int>::max()), "set ITER")
        ("SHOW", po::value<bool>(&showFlag)->default_value(false), "show results");

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);
    if (vm.count("help")) {
        cout << desc << "\n";
        return 1;
    }

    ofstream results_file("results.txt", ios::app);

    double error = 1.0;
    double *restrict A    = (double*)malloc(sizeof(double)*n*m);
    double *restrict Anew = (double*)malloc(sizeof(double)*n*m);

    nvtxRangePushA("init");
    initialize(A, Anew, m, n);
    nvtxRangePop();

    printf("Jacobi relaxation Calculation: %d x %d mesh, %lf tolerance %d max iters\n", n, m, tol, iter_max);
    results_file << "Jacobi relaxation Calculation: " << n << " x " << m << " mesh, " << tol << " tolerance " << iter_max << " max iters\n";

    auto start = chrono::high_resolution_clock::now();
    int iter = 0;

    nvtxRangePushA("while");
    while (error > tol && iter < iter_max )
    {
        nvtxRangePushA("calc");
        error = calcNext(A, Anew, m, n);
        nvtxRangePop();

        nvtxRangePushA("swap");
        swap(A, Anew, m, n);
        nvtxRangePop();

        if(iter % 100 == 0){
            fflush(stdout);
            printf("%lf >= %lf\t%d'i\r", error, tol, iter);
        }

        iter++;
    }
    printf("\33[2K\r");
    fflush(stdout);
    printf("%lf >= %lf\t%d'i\n", error, tol, iter);
    results_file << "Iterations" << iter << " s\n";

    nvtxRangePop();

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> runtime = end - start;

    printf("Time: %f s\n", runtime.count());
    results_file << "Time: " << runtime.count() << " s\n";

    if(showFlag){
        nvtxRangePushA("print_arr");
        print_arr(A, Anew, m, n);
        nvtxRangePop();
    }

    deallocate(A, Anew);
    results_file.close();

    return 0;
}

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

double calcNext(double *restrict A, double *restrict Anew, int m, int n){
    double error = 0.0;

    // Create cuBLAS handle
    cublasHandle_t handle;
    cublasCreate(&handle);

    // Allocate device memory for A and Anew
    double *d_A, *d_Anew;
    cudaMalloc((void**)&d_A, sizeof(double)*m*n);
    cudaMalloc((void**)&d_Anew, sizeof(double)*m*n);

    // Copy A and Anew from host to device
    cudaMemcpy(d_A, A, sizeof(double)*m*n, cudaMemcpyHostToDevice);
    cudaMemcpy(d_Anew, Anew, sizeof(double)*m*n, cudaMemcpyHostToDevice);

    // Perform reduction operation using cuBLAS
    double alpha = 1.0;
    double beta = 0.0;
    cublasDaxpy(handle, m*n, &alpha, d_A, 1, d_Anew, 1);
    cublasDnrm2(handle, m*n, d_Anew, 1, &error);
    cublasDnrm2(handle, m*n, d_A, 1, &alpha);
    error = fabs(error - alpha);

    // Copy Anew from device to host
    cudaMemcpy(Anew, d_Anew, sizeof(double)*m*n, cudaMemcpyDeviceToHost);

    // Free device memory
    cudaFree(d_A);
    cudaFree(d_Anew);

    // Destroy cuBLAS handle
    cublasDestroy(handle);

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
