from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from imager_images.forms import PhotoUpdateViewForm
from imager_images.models import Photo, Album



@login_required
def library(request):
    context = {'albums': request.user.albums.all()}
    return render(request, 'library.html', context)


# class LibraryForm(FormView):
#     def user_passes_test(self, request):
#         if request.user.is_authenticated():
#             self.object = self.get_object()
#             return self.object.user == request.user
#         return False

#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_passes_test(request):
#             return redirect_to_login(request.get_full_path())
#         return super(PhotoUpdateView, self).dispatch(
#             request, *args, **kwargs)

#     template_name = 'library.html'


@login_required
def stream(request):
    stream_users = [profile.user for profile in request.user.profile.following()]
    stream_users.append(request.user)
    context = {'photos': Photo.objects.filter(
        user__in=stream_users).filter(
        published__in=['pub', 'shd']).order_by('date_published')}
    return render(request, 'stream.html', context)


class AlbumCreate(CreateView):
    template_name = "new_album_form.html"
    model = Album
    fields = ['title', 'description', 'photos',  'published']


class AlbumUpdate(UpdateView):
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(PhotoUpdateView, self).dispatch(
            request, *args, **kwargs)

    model = Album
    field = ['title', 'description', 'published']


class AlbumDelete(DeleteView):
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(PhotoUpdateView, self).dispatch(
            request, *args, **kwargs)

    model = Album


class PhotoAddView(CreateView):
    template_name = 'photo_form.html'
    model = Photo
    fields = ('image',
              'title',
              'description',
              'published',
              )


class PhotoUpdateView(UpdateView):
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(PhotoUpdateView, self).dispatch(
            request, *args, **kwargs)

    form_class = PhotoUpdateViewForm
    model = Photo
    template_name = 'photo_form.html'


class PhotoDeleteView(DeleteView):
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(PhotoUpdateView, self).dispatch(
            request, *args, **kwargs)

    template_name = 'photo_confirm_delete.html'
    model = Photo
    success_url = reverse_lazy('images:library')
