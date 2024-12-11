#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    std::string s = argv[1];
    for (int i=0; i<s.size()/2; i++) {
        int j = s.size()-1-i;
        char tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
    std::cout << s << std::endl;
    return 0;
}
