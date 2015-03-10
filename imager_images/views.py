from django.shortcuts import render


def library(request):
    context = {'name': request.user}
    return render(request, 'library.html', context)
