from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def library(request):
    context = {'albums': request.user.albums.all()}
    # import pdb; pdb.set_trace()
    return render(request, 'library.html', context)
