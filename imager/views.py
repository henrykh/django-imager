from django.shortcuts import render
from imager_images.models import Photo


def home(request):
    # import pdb; pdb.set_trace()
    try:
        cover_photo_url = Photo.objects.filter(
            published='pub').order_by('?')[0].image.url
    except IndexError:
        cover_photo_url = "imager_images/Space_Needle002.jpg"
    context = {'cover_photo_url': cover_photo_url}
    return render(request, 'home.html', context)


def profile(request):
    context = {'name': request.user}
    return render(request, 'profile.html', context)


def activation_complete(request):
    context = {'name': request.user}
    return render(request, 'activation_complete.html', context)
