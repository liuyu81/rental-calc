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
        if i < 0:
            raise AssertionError("invalid polynomial")
        elif i > 0:
            df.append((c * i, i - 1))
        pass
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
    """polynomial for annual rental"""
    return ((v, i / d) for i in range(y))


def r2b(r, v=220.0, y=15, d=3):
    """cyclic increment to rental budget"""
    if r < 0:
        raise AssertionError("bad cyclic increment")
    f = list(g(v, y, d))
    return poly_eval(f, r + 1.0)


def b2r(b, v=220.0, y=15, d=3):
    """rental budget to cyclic increment"""
    if b < r2b(0.0, v, y, d):
        raise AssertionError("bad rental budget")
    f = [(-b, 0), ]
    f.extend(g(v, y, d))
    return (poly_root(f) - 1.0)


def console_main(args):
    """console interface"""
    if len(args) < 2:
        print("synopsis:")
        print(("  $ %s r2b increment(r) [first_year_rental(v) "
               "[rental_years(y) [years_per_cycle(d)]]]" % __file__))
        print(("  $ %s b2r budget(b) [first_year_rental(v) "
               "[rental_years(y) [years_per_cycle(d)]]]" % __file__))
        print("examples:")
        print(("  $ %s r2b 0.05 220 15 3" % __file__))
        print(("  %f" % r2b(0.05, 220.0, 15, 3)))
        print(("  $ %s b2r 4000.0 220 15 3" % __file__))
        print(("  %f" % b2r(4000.0, 220.0, 15, 3)))
        return os.EX_USAGE
    # parameters
    op = args[0].lower()
    a = float(args[1])  # r or b (per op)
    v = float(args[2]) if len(args) > 2 else 220.0
    y = int(args[3]) if len(args) > 3 else 15
    d = int(args[4]) if len(args) > 4 else 3
    # calculation
    if op == 'r2b':
        try:
            print((r2b(a, v, y, d)))
        except AssertionError as e:
            print((str(e)))
            return os.EX_USAGE
        pass
    if op == 'b2r':
        try:
            print((b2r(a, v, y, d)))
        except AssertionError as e:
            print((str(e)))
            return os.EX_USAGE
        pass
    return os.EX_OK


def django_main(request):
    """wsgi / django interface"""
    from django.http import HttpResponse
    from django.template import loader, Context
    # parameters
    data = request.REQUEST
    op = data[u"op"] if u"op" in data else u"r2b"
    r = float(data[u"r"].encode()) / 100.0 if u"r" in data else 0.05
    b = float(data[u"b"].encode()) if u"b" in data else 4000.0
    v = float(data[u"v"].encode()) if u"v" in data else 220.0
    y = int(data[u"y"].encode()) if u"y" in data else 15
    d = int(data[u"d"].encode()) if u"d" in data else 3
    err = u""
    # calculation
    if op == u"b2r":
        try:
            r = b2r(b, v, y, d)
        except AssertionError as e:
            r = 0.0
            err = unicode(e)
        pass
    if op == u"r2b":
        try:
            b = r2b(r, v, y, d)
        except AssertionError as e:
            b = 0.0
            err = unicode(e)
        pass
    # compose HTTP response
    response = HttpResponse(content_type='text/html')
    tmpl = loader.get_template('calc.html')
    cntx = Context({
        'v': v,
        'y': y,
        'd': d,
        'b': b,
        'r': r * 100.0,
        'r2b': op == u"r2b",
        'b2r': op == u"b2r",
        'err': err
    })
    response.write(tmpl.render(cntx))
    return response

if __name__ == '__main__':
    sys.exit(console_main(sys.argv[1:]))
