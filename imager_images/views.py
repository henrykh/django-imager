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
from imager_images.forms import (CreateAlbumViewForm,
                                 EditAlbumForm,
                                 PhotoUpdateViewForm,
                                 CreatePhotoViewForm,
                                 AddImageFormSet
                                 )
from imager_images.models import (Photo,
                                  Album
                                  )
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User





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


def album_create(request, *args, **kwargs):
    if request.POST:

        form = CreateAlbumViewForm(request.POST)
        if form.is_valid():
            kwargs['user'] = request.user
            album = form.save(**kwargs)
            add_image_formset = AddImageFormSet(
                request.POST, instance=album,
                )

            if add_image_formset.is_valid():
                album.save()
                add_image_formset.save()
                return HttpResponseRedirect(reverse(
                    'images:albumphoto_list', kwargs={'pk': album.pk}))
    else:
        form = CreateAlbumViewForm()
        # import pdb; pdb.set_trace()
        add_image_formset = AddImageFormSet(instance=Album(),
                                            queryset=Photo.albums.through.objects.filter(
                                                photo__user=request.user))
    return render_to_response("new_album_form.html", {
            "form": form,
            "add_image_formset": add_image_formset,
            }, context_instance=RequestContext(request))



# class AlbumCreate(CreateView):
#     template_name = "new_album_form.html"
#     model = Album
#     form_class = CreateAlbumViewForm

#     def get_form_kwargs(self):
#         kwargs = super(AlbumCreate, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def get_success_url(self):
#         return reverse('images:album_update', kwargs={'pk': self.object.pk})


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
    template_name = "new_photo_form.html"
    model = Photo
    form_class = CreatePhotoViewForm

    def get_form_kwargs(self):
        kwargs = super(PhotoAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('images:photo_update', kwargs={'pk': self.object.pk})

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
