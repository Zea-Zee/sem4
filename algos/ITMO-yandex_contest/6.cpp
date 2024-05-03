#include <iostream>
#include <vector>

using namespace std;

const int MOD = 1000000007;

int main() {
    int n, k;
    scanf("%d %d", &n, &k);

    vector<vector<int>> dp_even(n+1, vector<int>(k, 0));
    vector<vector<int>> dp_odd(n+1, vector<int>(k, 0));

    for (int digit = 1; digit <= 9; ++digit) {
        int remainder = digit % k;
        if (digit % 2 == 0) {
            dp_even[1][remainder]++;
        } else {
            dp_odd[1][remainder]++;
        }
    }

    for (int i = 2; i <= n; ++i) {
        for (int prev_remainder = 0; prev_remainder < k; ++prev_remainder) {
            for (int digit = 0; digit <= 9; ++digit) {
                int new_remainder = (prev_remainder * 10 + digit) % k;
                if (digit % 2 == 0) {
                    dp_even[i][new_remainder] = (dp_even[i][new_remainder] + dp_odd[i-1][prev_remainder]) % MOD;
                } else {
                    dp_odd[i][new_remainder] = (dp_odd[i][new_remainder] + dp_even[i-1][prev_remainder]) % MOD;
                }
            }
        }
    }


    int result = (dp_even[n][0] + dp_odd[n][0]) % MOD;
    printf("%d\n", result);
    return 0;
}
