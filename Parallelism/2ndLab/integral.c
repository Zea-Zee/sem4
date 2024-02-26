#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <omp.h>
#include <string.h>


const double PI = 3.14159265358979323846;
const double a = -4.0;
const double b = 4.0;
const int nsteps = 40000000;

double cpuSecond() {
    struct timespec ts;
    timespec_get(&ts, TIME_UTC);
    return ((double)ts.tv_sec + (double)ts.tv_nsec * 1.e-9);
}

double func(double x) {
    return exp(-x * x);
}

double integrate(double (*func)(double), double a, double b, int n) {
    double h = (b - a) / n;
    double sum = 0.0;
    for (int i = 0; i < n; i++)
        sum += func(a + h * (i + 0.5));
    sum *= h;
    return sum;
}

double integrate_omp(double (*func)(double), double a, double b, int n) {
    double h = (b - a) / n;
    double sum = 0.0;
#pragma omp parallel
    {
        int nthreads = omp_get_num_threads();
        int threadid = omp_get_thread_num();
        int items_per_thread = n / nthreads;
        int lb = threadid * items_per_thread;
        int ub = (threadid == nthreads - 1) ? (n - 1) : (lb + items_per_thread - 1);
        double sumloc = 0.0;
        for (int i = lb; i <= ub; i++)
            sumloc += func(a + h * (i + 0.5));
#pragma omp atomic
        sum += sumloc;
    }
    sum *= h;
    return sum;
}

double run_serial() {
    double t = cpuSecond();
    double res = 0;
    for (int i = 0; i < 50; i++)
        res += integrate(func, a, b, nsteps);
    t = (cpuSecond() - t) / 50;
    res /= 50;
    printf("Result (serial): %.12f; error %.12f\n", res, fabs(res - sqrt(PI)));
    return t;
}

double run_parallel() {
    double t = cpuSecond();
    double res = 0;
    for (int i = 0; i < 10; i++)
        res += integrate_omp(func, a, b, nsteps);
    t = (cpuSecond() - t) / 10;
    res /= 10;
    printf("Result (parallel): %.12f; error %.12f\n", res, fabs(res - sqrt(PI)));
    return t;
}

int main(int argc, char **argv) {
    // printf("Integration f(x) on [%.12f, %.12f], nsteps = %d\n", a, b, nsteps);
    double tserial = 0;
    if (argc == 1 || (argc > 1 && strcmp(argv[1], "-parallel") != 0)){
        tserial = run_serial();
        FILE *file = fopen("serial_integrate_time.txt", "w");
        fprintf(file, "%.6f", tserial);
        fclose(file);
    }


    if (argc > 1 && strcmp(argv[1], "-parallel") == 0){
        double tparallel = run_parallel();

        FILE *file = fopen("serial_integrate_time.txt", "r");
        double serialTime;
        fscanf(file, "%lf", &serialTime);
        printf("Speedup: %.2f\n", serialTime / tparallel);
    }

    return 0;
}
