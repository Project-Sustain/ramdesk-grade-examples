#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    int tot = 0;
    for (int i = 1; i < argc; i++) {
        tot += std::stoi(argv[i]);
    }
    std::cout << tot << std::endl;
    return 0;
}
