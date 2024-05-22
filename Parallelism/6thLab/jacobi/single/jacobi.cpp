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
#include <limits>


using namespace std;
namespace po = boost::program_options;

int main(int argc, char** argv){
    unsigned int n, m, iter_max;
    double tol;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "produce help message")
        ("NX", po::value<unsigned int>(&n)->default_value(128), "set NX")
        ("NY", po::value<unsigned int>(&m)->default_value(128), "set NY")
        ("TOLERANCE", po::value<double>(&tol)->default_value(1e-6), "set EPS")
        ("ITER", po::value<unsigned int>(&iter_max)->default_value(std::numeric_limits<unsigned int>::max()), "set ITER");

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

    printf("Jacobi relaxation Calculation: %d x %d mesh, %llf tolerance %d max iters\n", n, m, tol, iter_max);

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

        if(iter % 100 == 0){
            fflush(stdout);
            printf("%lf >= %lf\t%d'i\r", error, tol, iter);
        }

        iter++;
    }
    printf("\33[2K\r");
    fflush(stdout);
    printf("%lf >= %lf\t%d'i\n", error, tol, iter);

    nvtxRangePop();

    double runtime = omp_get_wtime() - st;

    printf("Time: %f s\n", runtime);

    deallocate(A, Anew);

    return 0;
}
