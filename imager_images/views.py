from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import (CreateView,
                                  UpdateView,
                                  DeleteView
                                  )
from django.core.urlresolvers import (reverse,
                                      reverse_lazy
                                      )
from django.contrib.auth.views import redirect_to_login
from imager_images.forms import (AlbumAddViewForm,
                                 AlbumUpdateViewForm,
                                 PhotoUpdateViewForm,
                                 PhotoAddViewForm,
                                 )
from imager_images.models import (Photo,
                                  Album
                                  )


@login_required
def library(request):
    try:
        photoNoAlb = request.user.photos.filter(albums__isnull=True).order_by('?')[0]
    except(IndexError):
        photoNoAlb = ''

    try:
        photoAll = request.user.photos.all().order_by('?')[0]
    except(IndexError):
        photoAll = ''

    default_cover = Photo()
    default_cover.image = 'imager_images/img/man.png'
    context = {'albums': request.user.albums.all(),
               'photoAll': photoAll,
               'photoNoAlb': photoNoAlb,
               'default': default_cover
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


class AlbumAddView(CreateView):
    template_name = "new_album_form.html"
    model = Album
    form_class = AlbumAddViewForm

    def get_initial(self):
        initial = super(AlbumAddView, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('images:albumphoto_list', kwargs={'pk': self.object.pk})


class AlbumUpdateView(UpdateView):
    template_name = "album_form.html"
    model = Album
    form_class = AlbumUpdateViewForm

    def get_success_url(self):
        return reverse('images:library')

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(AlbumUpdateView, self).dispatch(
            request, *args, **kwargs)


class AlbumDeleteView(DeleteView):
    model = Album

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(AlbumDeleteView, self).dispatch(
            request, *args, **kwargs)


class PhotoAddView(CreateView):
    template_name = "new_photo_form.html"
    model = Photo
    form_class = PhotoAddViewForm

    template_name = 'photo_form.html'
    model = Photo
    fields = ('image',
              'title',
              'description',
              'published',
              )

    def get_form_kwargs(self):
        kwargs = super(PhotoAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('images:loosephotos_list')


class PhotoUpdateView(UpdateView):

    form_class = PhotoUpdateViewForm
    model = Photo
    template_name = 'photo_form.html'

    def user_passes_test(self, request):
        # import ipdb; ipdb.set_trace()
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


class PhotoDeleteView(DeleteView):
    template_name = 'photo_confirm_delete.html'
    model = Photo

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(PhotoDeleteView, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET['src']
