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
                                 PhotoAddViewForm,
                                 PhotoUpdateViewForm,
                                 # PhotoDeleteViewForm,
                                 )
from imager_images.models import (Photo,
                                  Album
                                  )
from form_utils.widgets import ImageWidget


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
    default_cover.image = '/static/imager_images/img/man.png'
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
               'source': request.META['PATH_INFO'],
               'album': Photo.albums.through.album.get_queryset().filter(pk=pk)[0],
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
    model = Album
    form_class = AlbumAddViewForm

    def get_initial(self):
        # import ipdb; ipdb.set_trace()
        initial = super(AlbumAddView, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('images:albumphoto_list', kwargs={'pk': self.object.pk})
    template_name = "album_form.html"


class AlbumUpdateView(UpdateView):
    template_name = "album_form.html"
    model = Album
    form_class = AlbumUpdateViewForm

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

    def get_success_url(self):
        return self.request.GET['src']


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'photo_confirm_delete.html'

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

    def get_success_url(self):
        return reverse('images:library')


class PhotoAddView(CreateView):
    model = Photo
    form_class = PhotoAddViewForm
    template_name = 'photo_form.html'

    def get_form_kwargs(self):
        kwargs = super(PhotoAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('images:loosephotos_list')


class PhotoUpdateView(UpdateView):
    model = Photo
    form_class = PhotoUpdateViewForm
    template_name = 'photo_form.html'

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

    def form_valid(self, form):
        if form.has_changed():
            self.kwargs['changed_data'] = form.changed_data
            self.kwargs['cleaned_data'] = form.cleaned_data

        return super(PhotoUpdateView, self).form_valid(form)

    def get_success_url(self):
        try:
            if 'albums' in self.kwargs['cleaned_data']:
                if len(self.kwargs['cleaned_data']['albums']) > 1:
                    success_url = '/library/'
                else:
                    success_url = '/album/{}/'.format(
                        self.kwargs['cleaned_data']['albums'][0].pk)
        except KeyError:
            success_url = self.request.GET['src']

        return success_url


class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'photo_confirm_delete.html'

    def user_passes_test(self, request):
        import ipdb; ipdb.set_trace()
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
