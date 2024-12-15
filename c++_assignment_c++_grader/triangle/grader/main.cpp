#include "triangle.h"

#include <cmath>
#include <cstdlib>
#include <iostream>


double get_perimeter(double s1, double s2, double s3) {
    return s1 + s2 + s3;
}

double get_area(double s1, double s2, double s3) {
    double s = (s1 + s2 + s3) / 2.0;
    return std::sqrt(s * (s - s1) * (s - s2) * (s - s3));
}

bool is_equilateral(double s1, double s2, double s3) {
    return s1 == s2 && s2 == s3;
}

bool is_isosceles(double s1, double s2, double s3) {
    return s1 == s2 || s1 == s3 || s2 == s3;
}

bool is_scalene(double s1, double s2, double s3) {
    return s1 != s2 && s1 != s3 && s2 != s3;
}

double random_side()
{
    return 1.0 + (double) rand() / RAND_MAX * 99.0;
}

bool prob(double p)
{
    return (double) rand() / RAND_MAX < p;
}

int test(){
    double s1;
    double s2;
    double s3;
    double area;
    do {
        s1 = random_side();
        s2 = random_side();
        s3 = random_side();
        if (prob(0.3)) { // make it isosceles
            s2 = s1;
        }
        if (prob(0.3)) { // make it equilateral
            s3 = s1;
        }
        area = get_area(s1, s2, s3);
    } while (area != area); // make sure it's a valid triangle

    Triangle t(s1, s2, s3);
    t.print();
    
    int score = 0;
    if (t.get_perimeter() == get_perimeter(s1, s2, s3)) {
        score += 1;
    }
    if (t.get_area() == get_area(s1, s2, s3)) {
        score += 1;
    }
    if (t.is_equilateral() == is_equilateral(s1, s2, s3)) {
        score += 1;
    }
    if (t.is_isosceles() == is_isosceles(s1, s2, s3)) {
        score += 1;
    }
    if (t.is_scalene() == is_scalene(s1, s2, s3)) {
        score += 1;
    }

    if (score == 5) {
        std::cout << "Test passed" << std::endl;
    } else {
        std::cout << "Test failed" << std::endl;
    }
    return score;
}


int main() {
    srand(time(0));
    int score = 0;
    for (int i = 0; i < 20; i++) {
        score += test();
    }
    std::cout << score << std::endl;
    return 0;
}
