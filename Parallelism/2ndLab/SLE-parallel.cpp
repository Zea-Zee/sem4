#include <iostream>
#include <vector>

using namespace std;

void create_matrix_and_vector(int size, vector<vector<double>>& A, vector<double>& b) {
    A.resize(size, vector<double>(size, 1.0));
    for (int i = 0; i < size; ++i) {
        A[i][i] = 2.0;
    }

    b.resize(size, size + 1.0);
    cout << "Matrix is:\n";
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            cout << A[i][j];
        }
        cout << " " << b[i] << "\n";
    }
}


vector<double> simpleIteration(const vector<vector<double>>& A, const vector<double>& b, double epsilon = 1e-6, int maxIterations = 1000) {
    int n = A.size();
    vector<double> x(n, 0.0);

    vector<double> prev_x(n);
    int iter = 0;

    while (iter < maxIterations) {
        prev_x = x;

        for (int i = 0; i < n; ++i) {
            double sum = 0.0;
            for (int j = 0; j < n; ++j) {
                if (i != j) {
                    sum += A[i][j] * prev_x[j];
                }
            }
            x[i] = (b[i] - sum) / A[i][i];
        }

        double error = 0.0;
        for (int i = 0; i < n; ++i) {
            error += abs(x[i] - prev_x[i]);
        }
        if (error < epsilon) {
            break;
        }

        iter++;
    }

    cout << "Number of iterations: " << iter << endl;

    return x;
}

int main() {
    int size = 3;

    vector<vector<double>> A;
    vector<double> b;
    create_matrix_and_vector(size, A, b);

    vector<double> solution = simpleIteration(A, b);
    cout << "Solution:" << endl;
    for (int i = 0; i < solution.size(); ++i) {
        cout << "x[" << i << "] = " << solution[i] << endl;
    }

    return 0;
}
