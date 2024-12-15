#include "triangle.h"

#include <cmath>
#include <iostream>


Triangle::Triangle(double s1, double s2, double s3)
    : side1(s1), side2(s2), side3(s3) {}

double Triangle::get_perimeter() const {
    return side1 + side2 + side3;
}

double Triangle::get_area() const {
    double s = get_perimeter() / 2.0;
    return std::sqrt(s * (s - side1) * (s - side2) * (s - side3));
}

bool Triangle::is_equilateral() const {
    return side1 == side2 && side2 == side3;
}

bool Triangle::is_isosceles() const {
    return side1 == side2 || side1 == side3 || side2 == side3;
}

bool Triangle::is_scalene() const {
    return side1 != side2 && side1 != side3 && side2 != side3;
}
