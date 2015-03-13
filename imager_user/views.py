from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.views.generic import UpdateView
from django.core.urlresolvers import (reverse,
                                      reverse_lazy
                                      )
from imager_user.models import ImagerProfile
from imager_user.forms import ProfileUpdateViewForm


@login_required
def profile(request):
    context = {'name': request.user, 'profileID': request.user.profile.id}
    return render(request, 'profile.html', context)


@login_required
def profile_update(request):
    # import ipdb; ipdb.set_trace()
    context = {'request': request}
    return render(request, 'profile_edit.html', context)


class ProfileUpdateView(UpdateView):
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

    form_class = ProfileUpdateViewForm
    model = ImagerProfile
    template_name = 'profile_form.html'

# class ProfileEdit(UpdateView):
#     def user_passes_test(self, request):
#         if request.user.is_authenticated():
#             self.object = self.get_object()
#             return self.object.user == request.user
#         return False

#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_passes_test(request):
#             return redirect_to_login(request.get_full_path())
#         return super(ProfileEdit, self).dispatch(
#             request, *args, **kwargs)

#     def get_success_url(self):
#         return self.request.GET['src']

#     form_class = PhotoUpdateViewForm
#     model = ImagerProfile
#     template_name = 'profile_edit.html'
