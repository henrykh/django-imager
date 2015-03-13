from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from imager_images.forms import CreateAlbumForm, EditAlbumForm, PhotoUpdateViewForm
from imager_images.models import Photo, Album
from django.core.urlresolvers import reverse


@login_required
def library(request):
    # import ipdb; ipdb.set_trace()

    try:
        photoNoAlb = request.user.photos.filter(albums__isnull=True).order_by('?')[0]
    except(IndexError):
        photoNoAlb = ''

    try:
        photoAll = request.user.photos.all().order_by('?')[0]
    except(IndexError):
        photoAll = ''

    context = {'albums': request.user.albums.all(),
               'photoAll': photoAll,
               'photoNoAlb': photoNoAlb,
               }
    return render(request, 'library.html', context)


@login_required
def AlbumPhotoList(request, pk):
    context = {'photos': Photo.objects
               .filter(user=request.user)
               .filter(albums__pk=pk),
               'source': request.META['PATH_INFO']
               }
    return render(request, 'albumphoto_list.html', context)


@login_required
def LoosePhotosList(request):
    context = {'photos': request.user.photos.filter(albums__isnull=True),
               'source': request.META['PATH_INFO']
               }
    return render(request, 'loosephotos_list.html', context)


@login_required
def AllPhotosList(request):
    context = {'photos': request.user.photos.all(),
               'source': request.META['PATH_INFO']
               }
    return render(request, 'allphotos_list.html', context)


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
    form_class = CreateAlbumForm

    def get_form_kwargs(self):
        kwargs = super(AlbumCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('images:album_update', kwargs={'pk': self.object.pk})


class AlbumUpdate(UpdateView):
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(AlbumUpdate, self).dispatch(
            request, *args, **kwargs)

    template_name = "album_form.html"
    model = Album
    form = EditAlbumForm
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

    def get_success_url(self):
        return self.request.GET['src']

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
