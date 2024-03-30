#include <iostream>
#include <vector>

using namespace std;

// Функция решения системы линейных уравнений методом итераций
vector<double> solve_iterative(const vector<vector<double>>& A, const vector<double>& b, int max_iterations, double tolerance) {
    int n = A.size();
    vector<double> x(n, 0); // Инициализация начального приближения

    for (int k = 0; k < max_iterations; ++k) {
        vector<double> x_new(n, 0);
        for (int i = 0; i < n; ++i) {
            double sum = 0.0;
            for (int j = 0; j < n; ++j) {
                if (j != i) {
                    sum += A[i][j] * x[j];
                }
            }
            x_new[i] = (b[i] - sum) / A[i][i];
        }

        // Проверка на сходимость
        bool converged = true;
        for (int i = 0; i < n; ++i) {
            if (abs(x_new[i] - x[i]) > tolerance) {
                converged = false;
                break;
            }
        }

        if (converged) {
            cout << "Converged after " << k << " iterations." << endl;
            return x_new;
        }

        x = x_new;
    }

    cout << "Reached maximum iterations." << endl;
    return x;
}

int main() {
    // Задаем матрицу A и вектор b
    vector<vector<double>> A = {{4, 1, -1},
                                 {2, 7, 1},
                                 {1, -3, 12}};
    vector<double> b = {3, 19, 31};

    // Параметры метода итераций
    int max_iterations = 1000;
    double tolerance = 1e-6;

    // Решение системы линейных уравнений
    vector<double> solution = solve_iterative(A, b, max_iterations, tolerance);

    // Вывод результата
    cout << "Solution:" << endl;
    for (int i = 0; i < solution.size(); ++i) {
        cout << "x[" << i << "] = " << solution[i] << endl;
    }

    return 0;
}
