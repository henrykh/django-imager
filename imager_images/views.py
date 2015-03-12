from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imager_images.models import Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


@login_required
def library(request):
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


class PhotoAddView(CreateView):
    template_name = 'photo_form.html'
    model = Photo
    fields = ('image',
              'title',
              'description',
              'published',
              )


class PhotoUpdateView(UpdateView):
    template_name = 'photo_form.html'
    model = Photo

    fields = ('albums',
              'title',
              'description',
              'date_published',
              'published',
              )


class PhotoDeleteView(DeleteView):
    template_name = 'photo_form.html'
    model = Photo
    success_url = reverse_lazy('library')
