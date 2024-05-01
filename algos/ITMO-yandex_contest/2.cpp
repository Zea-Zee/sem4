#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
#include <iostream>

using namespace __gnu_pbds;
using namespace std;

typedef tree<int, null_type, greater<int>, rb_tree_tag, tree_order_statistics_node_update> ordered_set;

int main() {
    int n;
    cin >> n;

    ordered_set os;

    for (int i = 0; i < n; ++i) {
        int command, val;
        cin >> command >> val;

        if (command == 1)  os.insert(val);
        else if (command == -1) {
            auto it = os.find(val);
            os.erase(it);
        } else cout << *os.find_by_order(val - 1) << endl;
    }

    return 0;
}
