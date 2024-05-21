// PARAMETERS SECTION

// Enable или disable OpenACC
#define IS_ACC 1

// output file name
#define OUT_FILE "result.dat"

// параметры
#define TAU -0.01

// END OF PARAMETERS SECTION

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <chrono>
#include <boost/program_options.hpp>

using namespace std;
namespace po = boost::program_options;

unsigned int NX, NY, SIZE;
unsigned long long ITER;
double EPS;

// get matrix value (SIZE x SIZE)
double get_a(int row, int col) {
    if (row == col) return -4;
    if (row + 1 == col) return 1;
    if (row - 1 == col) return 1;
    if (row + NX == col) return 1;
    if (row - NX == col) return 1;
    return 0;
}

double get_b(int idx) {
    // some heat input/output
    if (idx == NY / 2 * NX + NX / 3) return 10;
    if (idx == NY * 2 / 3 * NX + NX * 2 / 3) return -25;
    return 0;
}

void init_matrix(double *M) {
    int i, j;

#if IS_ACC
#pragma acc parallel loop collapse(2)
#endif
    for (i = 0; i < SIZE; i++)
        for (j = 0; j < SIZE; j++)
            M[i * SIZE + j] = get_a(i, j);
}

void init_b(double *b) {
    int i;

#if IS_ACC
#pragma acc parallel loop
#endif
    for (i = 0; i < SIZE; i++)
        b[i] = get_b(i);
}

double norm(double *x) {
    double result = 0;
    int i;

#if IS_ACC
#pragma acc parallel loop reduction(+:result)
#endif
    for (i = 0; i < SIZE; i++)
        result += x[i] * x[i];

    return sqrt(result);
}

// res = Ax-y
void mul_mv_sub(double *res, double *A, double *x, double *y) {
    int i, j;

#if IS_ACC
#pragma acc parallel loop private(j)
#endif
    for (i = 0; i < SIZE; i++) {
        res[i] = -y[i];
        for (j = 0; j < SIZE; j++)
            res[i] += A[i * SIZE + j] * x[j];
    }
}

// x -= TAU * delta
void next(double *x, double *delta) {
    int i;

#if IS_ACC
#pragma acc parallel loop
#endif
    for (i = 0; i < SIZE; i++)
        x[i] -= TAU * delta[i];
}

void solve_simple_iter(double *A, double *x, double *b) {
    printf("solve_simple_iter\r",);

    double *Axmb, norm_b, norm_Axmb;

    norm_b = norm(b);

    Axmb = (double*)malloc(SIZE * sizeof(double));

    for(long long i = 0; i < ITER; i++) {
        mul_mv_sub(Axmb, A, x, b);
        norm_Axmb = norm(Axmb);
        if (norm_Axmb / norm_b < EPS) {
            break;
        }
        next(x, Axmb);
        if(i % 100 == 0) {
            fflush(stdout);
            printf("%lf >= %lf\t%lld\r", norm_Axmb / norm_b, EPS, i);
        }
    }

    printf("\33[2K\r");
    fflush(stdout);

    // for (int i = 0; i < SIZE; i++) {
    //     for (int j = 0; j < SIZE; j++) {
    //         cout << Axmb[i * j] << "\t\t";
    //     }
    //     cout << '\n';
    // }

    free(Axmb);
}

int main(int argc, char *argv[]) {
    // Define and parse command-line arguments
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "produce help message")
        ("NX", po::value<unsigned int>(&NX)->default_value(10), "set NX")
        ("NY", po::value<unsigned int>(&NY)->default_value(10), "set NY")
        ("TOLERANCE", po::value<double>(&EPS)->default_value(1e-5), "set EPS")
        ("ITER", po::value<unsigned long long>(&ITER)->default_value(1000), "set ITER");

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    if (vm.count("help")) {
        cout << desc << "\n";
        return 1;
    }

    SIZE = NX * NY;

    double *A, *b, *x;
    FILE *f;

    A = (double*)malloc(SIZE * SIZE * sizeof(double));
    b = (double*)malloc(SIZE * sizeof(double));
    x = (double*)malloc(SIZE * sizeof(double));

    auto start = std::chrono::high_resolution_clock::now();
    init_matrix(A);
    init_b(b);
    memset(x, 0, sizeof(double) * SIZE);
    solve_simple_iter(A, x, b);
    auto runtime = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::high_resolution_clock::now() - start);
    cout << "TIME: " << runtime.count() / 1000000. << endl;

    f = fopen(OUT_FILE, "wb");
    fwrite(x, sizeof(double), SIZE, f);
    fclose(f);

    free(A);
    free(b);
    free(x);

    return 0;
}


//./multi --NX 32 --NY 32 --EPS 1e-2 --ITER 1000000000
