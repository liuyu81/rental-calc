#!/usr/bin/env python
#
# Copyright (C) 2013, LIU Yu <liuyu@opencps.net>
# All rights reserved.
#

__all__ = ['r2b', 'b2r', ]

import os
import sys


def poly_eval(f, x):
    """evaluate the polynomial"""
    return sum([c * (x ** i) for c, i in f])


def poly_diff(f):
    """differentiate the polynomial"""
    df = []
    for c, i in f:
        if i > 0:
            df.append((c * i, i - 1))
    return df


def poly_root(f, initial=1.05, eps=0.000001):
    """Newton's method for root finding"""
    df = poly_diff(f)
    x = None
    x_n = initial
    while True:
        x = x_n
        x_n = x - (float(poly_eval(f, x)) / poly_eval(df, x))
        if (abs(x - x_n) < eps):
            break
    return x_n


def g(v, y, d):
    """polynomial"""
    p = []
    for i in range(y):
        p.append((v, i / d))
    return p


def r2b(r, v=220.00, y=15, d=3):
    """cyclic increment to rental budget"""
    if r < 0:
        raise ValueError("bad increment")
    assert(r >= 0)
    f = g(v, y, d)
    return poly_eval(f, 1.0 + r)


def b2r(b, v=220.00, y=15, d=3):
    "rental budget to cyclic increment"
    if b < r2b(0.00, v, y, d):
        raise ValueError("bad rental budget")
    f = g(v, y, d)
    f.append((-b, 0))
    return (poly_root(f) - 1.0)


def main(args):
    if len(args) < 2:
        print(("synopsis: %s r2b rate(r) [first_year_rental(v) "
               "[years(y) [years_per_cycle(d)]]]" % __file__))
        print(("          %s b2r budget(b) [first_year_rental(v) "
               "[years(y) [years_per_cycle(d)]]]" % __file__))
        print("examples:")
        print(("  $ %s r2b 0.05 220 15 3" % __file__))
        print(("  %f" % r2b(0.05, 220.0, 15, 3)))
        print(("  $ %s b2r 4000.0 220 15 3" % __file__))
        print(("  %f" % b2r(4000.0, 220.0, 15, 3)))
        return os.EX_USAGE
    # parameters
    op = b2r if args[0].lower() == 'b2r' else r2b
    a = float(args[1])  # r or b (per op)
    v = float(args[2]) if len(args) > 2 else 220.00
    y = int(args[3]) if len(args) > 3 else 15
    d = int(args[4]) if len(args) > 4 else 3
    # calculation
    try:
        print((op(a, v, y, d)))
    except ValueError as e:
        print((str(e)))
        return os.EX_USAGE
    return os.EX_OK


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
