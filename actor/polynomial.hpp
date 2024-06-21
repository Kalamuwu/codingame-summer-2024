#ifndef POLYNOMIALH
#define POLYNOMIALH

#include "costs.hpp"

/**
 * Polynomial: A struct wrapping n float values, representing a polynomial of
 * degree n.
 * Represents ax^3 + bx^2 + cx + d.
 */
struct Polynomial
{
    Polynomial() :
        a(0), b(0), c(0), d(0) {}
    Polynomial
        (const double D) :
        a(0), b(0), c(0), d(D) {}
    Polynomial
        (const double C,
         const double D) :
         a(0), b(0), c(C), d(D) {}
    Polynomial
        (const double B,
         const double C,
         const double D) :
         a(0), b(B), c(C), d(D) {}
    Polynomial
        (const double A,
         const double B,
         const double C,
         const double D) :
         a(A), b(B), c(C), d(D) {}

    double evaluate(const double k)
    {
        return a * k*k*k
             + b * k*k
             + c * k
             + d;
    }

    Costs evaluate(const Costs k)
    {
        return Costs(
            evaluate(k.UP),
            evaluate(k.DOWN),
            evaluate(k.LEFT),
            evaluate(k.RIGHT));
    }

    double a, b, c, d;
};

#endif // POLYNOMIALH
