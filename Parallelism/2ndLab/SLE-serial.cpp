#include <iostream>
#include <vector>
#include <cmath>
#include <omp.h>

using namespace std;

double calculateNewX(const vector<vector<double>>& A, const vector<double>& b, const vector<double>& x, int i) {
    double sum = 0.0;
    int N = x.size();
    for (int j = 0; j < N; ++j) {
        if (j != i) {
            sum += A[i][j] * x[j];
        }
    }
    return (b[i] - sum) / A[i][i];
}

// Функция для проверки сходимости итерационного процесса
bool checkConvergence(const vector<double>& newX, const vector<double>& oldX, double epsilon) {
    int N = newX.size();
    for (int i = 0; i < N; ++i) {
        if (abs(newX[i] - oldX[i]) > epsilon) {
            return false; // Итерационный процесс еще не сошелся
        }
    }
    return true; // Итерационный процесс сошелся
}

int main(int argc, char* argv[]) {
    int N = 1000; // Размерность матрицы и вектора по умолчанию

    // Проверяем наличие аргументов командной строки
    if (argc >= 2) {
        if (string(argv[1]) == "-N" && argc >= 3) {
            N = stoi(argv[2]);
        }
    }

    // Инициализация матрицы A и вектора b
    vector<vector<double>> A(N, vector<double>(N, 1.0));
    vector<double> b(N, N + 1.0);
    for (int i = 0; i < N; ++i) {
        A[i][i] = 2.0;
    }

    // Начальное приближение для вектора x
    vector<double> x(N, 0.0);

    // Параметры для сходимости итерационного процесса
    double epsilon = 1e-6;
    int maxIterations = 100000;

// Итерационный процесс
    int iterations = 0;
    bool converged = false;
    while (iterations < maxIterations && !converged) {
        // Инициализируем newX перед началом каждой итерации
        vector<double> newX(N);

        // Сохраняем предыдущее значение x
        vector<double> oldX = x;

        // Вычисляем новое значение x для каждого элемента параллельно
        #pragma omp parallel for
        for (int i = 0; i < N; ++i) {
            newX[i] = calculateNewX(A, b, x, i);
        }

        // Проверяем сходимость
        converged = checkConvergence(newX, oldX, epsilon);

        // Обновляем значение x
        x = newX;

        iterations++;
    }

    // Выводим результат
    cout << "Solution after " << iterations << " iterations:" << endl;
    for (int i = 0; i < N; ++i) {
        cout << "x[" << i << "] = " << x[i] << endl;
    }

    return 0;
}
