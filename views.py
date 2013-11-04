from django.http import HttpResponse
from django.template import loader, Context

def calc(request):
    import calc as plan
    data = request.REQUEST
    op = data[u"op"] if u"op" in data else u'r2b'
    v = float(data[u"v"].encode()) if u"v" in data else 220
    y = int(data[u"y"].encode()) if u"y" in data else 15
    d = int(data[u"d"].encode()) if u"d" in data else 3
    r = float(data[u"r"].encode()) / 100.0 if u"r" in data else 0.05
    b = float(data[u"b"].encode()) if u"b" in data else 4000.00
    err = u""
    if op == u'b2r':
        try:
            r = plan.b2r(b, v, y, d)
        except ValueError as e:
            err = u"bad budget"
            r = 0.0
    if op == u'r2b':
        try:
            b = plan.r2b(r, v, y, d)
        except ValueError as e:
            err = u"bad rate"
            b = 0.0
    cntx = Context({
        'v': v,
        'y': y,
        'd': d,
        'b': b,
        'r': r * 100.0,
        'r2b': u"checked=checked" if op == u"r2b" else u"",
        'b2r': u"checked=checked" if op == u"b2r" else u"",
        'err': err
    })
    tmpl = loader.get_template('calc.txt')
    response = HttpResponse(content_type='text/html')
    response.write(tmpl.render(cntx))
    return response
