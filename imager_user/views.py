from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from imager_user.models import ImagerProfile
from imager_user.forms import ProfileUpdateViewForm
from django.contrib.auth.models import User


@login_required
def profile(request):
    photo_count = len(request.user.photos.all())
    album_count = len(request.user.albums.all())
    follower_count = len(ImagerProfile.objects.filter(
        follows=request.user.profile))
    context = {'name': request.user, 'profileID': request.user.profile.id,
               'photo_count': photo_count, "album_count": album_count,
               "follower_count": follower_count}
    return render(request, 'profile.html', context)


class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdateViewForm
    model = ImagerProfile
    template_name = 'profile_form.html'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect_to_login(request.get_full_path())
        return super(ProfileUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile:profile')


def PublicProfile(request, pk):
    context = {'selected_user': User.objects.get(pk=pk)}
    return render(request, 'public_profile.html', context)
