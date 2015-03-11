from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_images.models import Photo

@login_required
def library(request):
    # import pdb; pdb.set_trace();
    context = {'albums': request.user.albums.all()}
    return render(request, 'library.html', context)


@login_required
def stream(request):
    stream_users = [profile.user for profile in request.user.profile.following()]
    stream_users.append(request.user)
    context = {'photos': Photo.objects.filter(
        user__in=stream_users).filter(
        published__in=['pub', 'shd']).order_by('date_published')}
    return render(request, 'stream.html', context)
