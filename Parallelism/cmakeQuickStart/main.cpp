#include <iostream>
#include <cmath>
#include <cstdlib>
#include <vector>

#define PI 3.14159265358979323846
#define period 2 * PI
#define SIZE 10000000

using namespace std;

template <typename T>
void fillVectorWithSin(vector<T> &vec){
    for(int i = 0; i < vec.size(); i++){
        vec[i] = static_cast<T>(sin(period * i) / vec.size());
    }
}

template <typename T>
T computeVectorSum(vector<T> &vec){
    T sum = 0;
    for(int i = 0; i < vec.size(); i++){
        sum += vec[i];
    }
    return sum;
}

int main(){
    #ifdef USE_DOUBLE
        using DataType = double;
        cout << "Using double";
    #else 
        using DataType = float;
        cout << "Using float";
    #endif
    vector<DataType> vec(SIZE);
    fillVectorWithSin(vec);
    cout << computeVectorSum(vec);
    return 0;
}