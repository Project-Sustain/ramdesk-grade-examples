#ifndef TRIANGLE_H
#define TRIANGLE_H

#include <iostream>

class Triangle {
private:
    double side1, side2, side3;

public:
    Triangle(double s1, double s2, double s3);
    double get_perimeter() const;
    double get_area() const;
    bool is_equilateral() const;
    bool is_isosceles() const;
    bool is_scalene() const;
    void print() const {
        std::cout << "Triangle" << std::endl;
        std::cout << "Sides: " << side1 << ", " << side2 << ", " << side3 << std::endl;
        std::cout << "Perimeter: " << get_perimeter() << std::endl;
        std::cout << "Area: " << get_area() << std::endl;
        std::cout << "Equilateral: " << is_equilateral() << std::endl;
        std::cout << "Isosceles: " << is_isosceles() << std::endl;
        std::cout << "Scalene: " << is_scalene() << std::endl;
    }
};

#endif
