#include <stdio.h>
#include <stdlib.h>


int main(int argc, char** args) {
    int number = atoi(args[1]);
    int factorial = 1;
    for (int i = 2; i <= number; i++) {
        factorial *= i;
    }
    printf("%d\n", factorial);
}
