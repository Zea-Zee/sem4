#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <omp.h>
#include "laplace2d.hpp"
#include <nvtx3/nvToolsExt.h>
#include <boost/program_options.hpp>
#include <chrono>
#include <iostream>
#include <fstream>
#include <limits>

#include <cublas_v2.h>
#include <cuda_runtime.h>


using namespace std;
namespace po = boost::program_options;

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
    results_file << "Jacobi relaxation Calculation: " << n << " x " << m << " mesh, " << tol << " tolerance " << iter_max << " max iters\n";  // Запись в файл

    auto start = chrono::high_resolution_clock::now();
    int iter = 0;

    cublasHandle_t handle;
    cublasCreate(&handle);

    nvtxRangePushA("while");
    while (error > tol && iter < iter_max )
    {
        nvtxRangePushA("calc");
        error = calcNext(A, Anew, m, n, handle);
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
