#ifndef COSTS_H
#define COSTS_H

#include <stdint.h>
#include <iostream>

/**
 * Costs: A struct wrapping 4 float values, representing the cost associated
 *        with actions `UP`, `DOWN`, `LEFT`, and `RIGHT`, respectively. Also
 *        defines a few operators, for ease of use.
 */
struct Costs
{
    Costs() : UP(0), DOWN(0), LEFT(0), RIGHT(0) {}
    Costs(const double k) : UP(k), DOWN(k), LEFT(k), RIGHT(k) {}
    Costs(const double up,   const double down,    \
          const double left, const double right) : \
          UP(up), DOWN(down), LEFT(left), RIGHT(right) {}

    inline Costs& operator+=(const Costs& c2);
    inline Costs& operator-=(const Costs& c2);
    inline Costs& operator*=(const Costs& c2);
    inline Costs& operator/=(const Costs& c2);
    inline Costs& operator+=(const double k);
    inline Costs& operator-=(const double k);
    inline Costs& operator*=(const double k);
    inline Costs& operator/=(const double k);

    inline void debugPrint();

    double UP, DOWN, LEFT, RIGHT;
};

inline void Costs::debugPrint()
{
    fprintf(stderr, "  UP    %.3f\n", UP);
    fprintf(stderr, "  DOWN  %.3f\n", DOWN);
    fprintf(stderr, "  LEFT  %.3f\n", LEFT);
    fprintf(stderr, "  RIGHT %.3f\n", RIGHT);
}

inline Costs& Costs::operator+=(const Costs& c2)
{
    UP    += c2.UP;
    DOWN  += c2.DOWN;
    LEFT  += c2.LEFT;
    RIGHT += c2.RIGHT;
    return *this;
}

inline Costs& Costs::operator-=(const Costs& c2)
{
    UP    -= c2.UP;
    DOWN  -= c2.DOWN;
    LEFT  -= c2.LEFT;
    RIGHT -= c2.RIGHT;
    return *this;
}

inline Costs& Costs::operator*=(const Costs& c2)
{
    UP    *= c2.UP;
    DOWN  *= c2.DOWN;
    LEFT  *= c2.LEFT;
    RIGHT *= c2.RIGHT;
    return *this;
}

inline Costs& Costs::operator/=(const Costs& c2)
{
    UP    /= c2.UP;
    DOWN  /= c2.DOWN;
    LEFT  /= c2.LEFT;
    RIGHT /= c2.RIGHT;
    return *this;
}

inline Costs& Costs::operator+=(const double k)
{
    UP    += k;
    DOWN  += k;
    LEFT  += k;
    RIGHT += k;
    return *this;
}

inline Costs& Costs::operator-=(const double k)
{
    UP    -= k;
    DOWN  -= k;
    LEFT  -= k;
    RIGHT -= k;
    return *this;
}

inline Costs& Costs::operator*=(const double k)
{
    UP    *= k;
    DOWN  *= k;
    LEFT  *= k;
    RIGHT *= k;
    return *this;
}

inline Costs& Costs::operator/=(const double k)
{
    double t = 1.0 / k;
    UP    *= t;
    DOWN  *= t;
    LEFT  *= t;
    RIGHT *= t;
    return *this;
}

inline Costs operator+(const Costs& c1, const Costs& c2)
{
    return {
        (c1.UP    + c2.UP),
        (c1.DOWN  + c2.DOWN),
        (c1.LEFT  + c2.LEFT),
        (c1.RIGHT + c2.RIGHT),
    };
}

inline Costs operator-(const Costs& c1, const Costs& c2)
{
    return {
        (c1.UP    - c2.UP),
        (c1.DOWN  - c2.DOWN),
        (c1.LEFT  - c2.LEFT),
        (c1.RIGHT - c2.RIGHT),
    };
}

inline Costs operator*(const Costs& c1, const Costs& c2)
{
    return {
        (c1.UP    * c2.UP),
        (c1.DOWN  * c2.DOWN),
        (c1.LEFT  * c2.LEFT),
        (c1.RIGHT * c2.RIGHT),
    };
}

inline Costs operator/(const Costs& c1, const Costs& c2)
{
    return {
        (c1.UP    / c2.UP),
        (c1.DOWN  / c2.DOWN),
        (c1.LEFT  / c2.LEFT),
        (c1.RIGHT / c2.RIGHT),
    };
}

inline Costs operator+(const Costs& c, const double k)
{
    return {
        (c.UP    + k),
        (c.DOWN  + k),
        (c.LEFT  + k),
        (c.RIGHT + k),
    };
}

inline Costs operator-(const Costs& c, const double k)
{
    return {
        (c.UP    - k),
        (c.DOWN  - k),
        (c.LEFT  - k),
        (c.RIGHT - k),
    };
}

inline Costs operator*(const Costs& c, const double k)
{
    return {
        (c.UP    * k),
        (c.DOWN  * k),
        (c.LEFT  * k),
        (c.RIGHT * k),
    };
}

inline Costs operator/(const Costs& c, const double k)
{
    double t = 1.0 / k;
    return {
        (c.UP    - t),
        (c.DOWN  - t),
        (c.LEFT  - t),
        (c.RIGHT - t),
    };
}

#endif // COSTS_H
