from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.shortcuts import render
from imager_images.models import Photo
import os
from django.conf import settings

# def stub(request, *args, **kwargs):
#     body = 'Stub View\n\n'
#     if args:
#         body += 'Args:\n'
#         body += '\n'.join(['\t%s' % a for a in args])
#     if kwargs:
#         body += 'Kwargs:\n'
#         body += '\n'.join(['\t%s: %s' % i for i in kwargs.items()])
#     return HttpResponse(body, content_type='text/plain')


def home(request):
    # import pdb; pdb.set_trace()
    cover_photo = Photo.objects.filter(published='pub').order_by('?')[0]
    cover_photo_path = os.path.join(settings.MEDIA_URL, cover_photo.image.name)
    context = {'name': 'bob', 'cover_photo_path': cover_photo_path}
    return render(request, 'home.html', context)
