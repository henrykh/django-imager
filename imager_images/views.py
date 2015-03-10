from django.shortcuts import render


def library(request):
    context = {'albums': request.user.albums.all(), 'test': request.user.albums.all()[0]}
    # import pdb; pdb.set_trace()
    return render(request, 'library.html', context)
