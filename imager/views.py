import HttpResponse


def stub(request, *args, **kwargs):
    body = 'Stub View\n\n'
    if args:
        body += 'Args:\n'
        body += '\n'.join(['\t%s' % a for a in args])
    if kwargs:
        body += 'Kwargs:\n'
        body += '\n'.join(['\t%s: %s' % i for i in kwargs.items()])
    return HttpResponse()
