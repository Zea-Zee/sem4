#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include "laplace2d.h"
#include <nvtx3/nvToolsExt.h>
#include <boost/program_options.hpp>
#include <chrono>

namespace po = boost::program_options;

int main(int argc, char** argv){
    int n, m, max_iter;
    double tol;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "produce help message")
        ("NX", po::value<unsigned int>(&N)->default_value(10), "set NX")
        ("NY", po::value<unsigned int>(&m)->default_value(10), "set NY")
        ("TOLERANCE", po::value<double>(&tol)->default_value(1e-5), "set EPS")
        ("ITER", po::value<unsigned long long>(&I)->default_value(1000), "set ITER");

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);
    if (vm.count("help")) {
        cout << desc << "\n";
        return 1;
    }

    
    double error = 1.0;
    double *restrict A    = (double*)malloc(sizeof(double)*n*m);
    double *restrict Anew = (double*)malloc(sizeof(double)*n*m);

    nvtxRangePushA("init");
    initialize(A, Anew, m, n);
    nvtxRangePop();

    printf("Jacobi relaxation Calculation: %d x %d mesh\n", n, m);

    double st = omp_get_wtime();
    int iter = 0;

    nvtxRangePushA("while");
    while ( error > tol && iter < iter_max )
    {
        nvtxRangePushA("calc");
        error = calcNext(A, Anew, m, n);
        nvtxRangePop();

        nvtxRangePushA("swap");
        swap(A, Anew, m, n);
        nvtxRangePop();

        if(iter % 100 == 0) printf("%5d, %0.6f\n", iter, error);

        iter++;
    }
    nvtxRangePop();

    double runtime = omp_get_wtime() - st;

    printf(" total: %f s\n", runtime);

    deallocate(A, Anew);

    return 0;
}
